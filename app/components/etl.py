import pandas as pd
import re
from app.models import DataFklim
from app.exts import db
from sqlalchemy.exc import SQLAlchemyError
import calendar

def proses_data(df):
    df.columns = df.columns.str.lower().str.replace(' (%)', '')

    def bersihkan_str_float(var):
        var = var.apply(lambda x: re.sub(r'[^\d\.]+', '', str(x)) if isinstance(x, str) else x)
        return pd.to_numeric(var, errors='coerce')

    for col in df.columns:
        if df[col].dtype == 'object' and col != 'cuaca' and col != 'namasta':
            df[col] = bersihkan_str_float(df[col])

    for col in df.columns:
        if col != 'cuaca' and col != 'namasta':
            df[col] = df[col].fillna(df[col].mean())

    df = df.drop_duplicates()

    df['waktu'] = pd.to_datetime({'year': df['tahun'], 'month': df['bulan'], 'day': df['tgl']})

    numerikal = ['anginarahrata', 'suhu7', 'suhu18', 'tgl', 'anginkecrata', 'tahun', 
                 'curahhujan', 'tekananudara', 'bulan', 'kelembapan18', 'anginarah', 
                 'suhumaks', 'suhumin', 'suhurata', 'kelembapan7', 'suhu13', 
                 'sinarmatahari', 'kelembapanrata', 'anginkecmaks', 'kelembapan13']
    for kolom in numerikal:
        if kolom in df.columns:
            df[kolom] = df[kolom].apply(lambda x: 0 if x < -2100 or x > 2100 else x)

    df['bulan_teks'] = df['bulan'].apply(lambda x: calendar.month_abbr[x] if pd.notna(x) else '')

    kelembapan_cols = ['kelembapan7', 'kelembapan13', 'kelembapan18']
    if all(col in df.columns for col in kelembapan_cols):
        df['kelembapanmaks'] = df[kelembapan_cols].max(axis=1)
        df['kelembapanmin'] = df[kelembapan_cols].min(axis=1)

    return df

def etl_process(file_path):
    try:
        df = pd.read_csv(file_path)

        df = proses_data(df)

        last_record = db.session.query(DataFklim).order_by(DataFklim.waktu.desc()).first()
        
        if last_record:
            last_year = last_record.tahun
            last_month = last_record.bulan
            if not ((df['tahun'].iloc[0] > last_year) or 
                    (df['tahun'].iloc[0] == last_year and df['bulan'].iloc[0] >= last_month)):
                return "Data tidak memenuhi syarat tahun atau bulan terbaru."

        for _, row in df.iterrows():
            if not db.session.query(DataFklim).filter_by(
                tahun=row['tahun'], bulan=row['bulan'], tgl=row['tgl']
            ).first():
                new_record = DataFklim(**row.to_dict())
                db.session.add(new_record)

        db.session.commit()
        return "Data berhasil ditambahkan ke database."

    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Kesalahan terjadi: {e}"

    except Exception as e:
        return f"Kesalahan umum: {e}"