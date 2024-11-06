import pandas as pd
from app.models import DataFklim
from app.components.windrose import get_range

def kpi_iklim(tahun=None, session=None):
    df = pd.DataFrame([data.to_dict() for data in session.query(DataFklim).all()])

    if tahun is None:
        tahun_range = df['tahun'].unique()
    elif isinstance(tahun, str):
        tahun_range = [int(tahun)]
    elif isinstance(tahun, list) or isinstance(tahun, tuple):
        if len(tahun) == 1:
            tahun_range = list(tahun)
        elif len(tahun) == 2:
            tahun_range = list(range(int(tahun[0]), int(tahun[1]) + 1))
        else:
            raise ValueError("Input tahun harus berupa satu tahun atau dua tahun")
    else:
        raise ValueError("Input untuk tahun harus berupa string, list, atau tuple")

    df_year = df[df['tahun'].isin(tahun_range)]

    kpi_data = []

    def calculate_kpi(column, parameter):
        max_val = df_year[column].max()
        idx_max = df_year[column].idxmax()
        tanggal_max = f"{df_year.loc[idx_max, 'tgl']} {df_year.loc[idx_max, 'bulan_teks']} {df_year.loc[idx_max, 'tahun']}"
        cuaca_max = df_year.loc[idx_max, 'cuaca']

        min_val = df_year[column].min()
        idx_min = df_year[column].idxmin()
        tanggal_min = f"{df_year.loc[idx_min, 'tgl']} {df_year.loc[idx_min, 'bulan_teks']} {df_year.loc[idx_min, 'tahun']}"
        cuaca_min = df_year.loc[idx_min, 'cuaca']

        return [
            {'parameter': f"{parameter} Tertinggi", 'nilai': max_val, 'tanggal': tanggal_max, 'cuaca': cuaca_max},
            {'parameter': f"{parameter} Terendah", 'nilai': min_val, 'tanggal': tanggal_min, 'cuaca': cuaca_min}
        ]

    columns = ['curahhujan', 'suhumaks', 'suhumin', 'kelembapanmaks', 'kelembapanmin', 'tekananudara', 'anginkecmaks', 'anginkecrata']
    parameters = ['Curah Hujan Harian', 'Suhu Maksimum', 'Suhu Minimum', 'Kelembapan Relatif (RH) Maksimum', 'Kelembapan Relatif (RH) Minimum', 'Tekanan Udara', 'Kecepatan Angin', 'Kecepatan Angin Rata-rata']

    for column, parameter in zip(columns, parameters):
        kpi_data.extend(calculate_kpi(column, parameter))

    return kpi_data

def kpi_iklim_bulan(tahun=None, bulan=None, session=None):
    df = pd.DataFrame([data.to_dict() for data in session.query(DataFklim).all()])
    
    # Menggunakan fungsi get_range yang sudah ada
    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    # Filter dataframe berdasarkan tahun dan bulan
    df_filtered = df[
        (df['tahun'].isin(tahun_range)) & 
        (df['bulan'].isin(bulan_range))
    ]

    kpi_data = []

    def calculate_kpi(column, parameter):
        max_val = df_filtered[column].max()
        idx_max = df_filtered[column].idxmax()
        tanggal_max = f"{df_filtered.loc[idx_max, 'tgl']} {df_filtered.loc[idx_max, 'bulan_teks']} {df_filtered.loc[idx_max, 'tahun']}"
        cuaca_max = df_filtered.loc[idx_max, 'cuaca']

        min_val = df_filtered[column].min()
        idx_min = df_filtered[column].idxmin()
        tanggal_min = f"{df_filtered.loc[idx_min, 'tgl']} {df_filtered.loc[idx_min, 'bulan_teks']} {df_filtered.loc[idx_min, 'tahun']}"
        cuaca_min = df_filtered.loc[idx_min, 'cuaca']

        return [
            {'parameter': f"{parameter} Tertinggi", 'nilai': max_val, 'tanggal': tanggal_max, 'cuaca': cuaca_max},
            {'parameter': f"{parameter} Terendah", 'nilai': min_val, 'tanggal': tanggal_min, 'cuaca': cuaca_min}
        ]

    columns = ['curahhujan', 'suhumaks', 'suhumin', 'kelembapanmaks', 'kelembapanmin', 
               'tekananudara', 'anginkecmaks', 'anginkecrata']
    parameters = ['Curah Hujan Harian', 'Suhu Maksimum', 'Suhu Minimum', 
                 'Kelembapan Relatif (RH) Maksimum', 'Kelembapan Relatif (RH) Minimum', 
                 'Tekanan Udara', 'Kecepatan Angin', 'Kecepatan Angin Rata-rata']

    for column, parameter in zip(columns, parameters):
        kpi_data.extend(calculate_kpi(column, parameter))

    return kpi_data