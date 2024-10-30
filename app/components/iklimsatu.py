import calendar
import pandas as pd
from app.models import DataFklim

def prepare_suhu_data(tahun=None, session=None):
    # Mendapatkan data dari database
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])
    
    # Mengonversi tahun ke list yang dapat diolah
    if tahun is None:
        tahun_range = df['tahun'].unique()
    elif isinstance(tahun, str):
        tahun_range = [int(tahun)]
    elif isinstance(tahun, list) or isinstance(tahun, tuple):
        tahun_range = list(range(int(tahun[0]), int(tahun[1]) + 1))
    else:
        raise ValueError("Input tahun harus berupa string, list, atau tuple")

    # Memilih data sesuai tahun yang dipilih
    df_year = pd.concat([df[df['tahun'] == t] for t in tahun_range])
    df_year = df_year[(df_year['suhurata'] != 0) & (df_year['suhumaks'] != 0) & (df_year['suhumin'] != 0)]
    df_year['bulan'] = df_year['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    # Menghitung statistik suhu per bulan
    suhu_rata_rata = df_year.groupby('bulan')['suhurata'].mean().reset_index()
    suhu_maks_abs = df_year.groupby('bulan')['suhumaks'].max().reset_index()
    suhu_maks = df_year.groupby('bulan')['suhumaks'].mean().reset_index()
    suhu_min = df_year.groupby('bulan')['suhumin'].mean().reset_index()
    suhu_min_abs = df_year.groupby('bulan')['suhumin'].min().reset_index()
    
    # Urutkan berdasarkan bulan
    months = calendar.month_abbr[1:13]
    for df in [suhu_rata_rata, suhu_maks_abs, suhu_maks, suhu_min, suhu_min_abs]:
        df['bulan'] = pd.Categorical(df['bulan'], categories=months, ordered=True)
        df.sort_values('bulan', inplace=True)

    # Mengisi nilai NaN dengan rata-rata kolom yang bersangkutan
    suhu_rata_rata['suhurata'].fillna(suhu_rata_rata['suhurata'].mean(), inplace=True)
    suhu_maks_abs['suhumaks'].fillna(suhu_maks_abs['suhumaks'].mean(), inplace=True)
    suhu_maks['suhumaks'].fillna(suhu_maks['suhumaks'].mean(), inplace=True)
    suhu_min['suhumin'].fillna(suhu_min['suhumin'].mean(), inplace=True)
    suhu_min_abs['suhumin'].fillna(suhu_min_abs['suhumin'].mean(), inplace=True)

    # Menggabungkan data untuk dikirim dalam format JSON
    data2 = {
        'labels': suhu_rata_rata['bulan'].tolist(),
        'datasets': [
            {
                'label': 'Suhu Rata-Rata',
                'data': suhu_rata_rata['suhurata'].round(2).tolist(),
                'borderColor': 'rgba(255, 99, 132, 1)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderWidth': 2,
                'fill': True
            },
            {
                'label': 'Suhu Maksimum Absolut',
                'data': suhu_maks_abs['suhumaks'].round(2).tolist(),
                'borderColor': 'rgba(54, 162, 235, 1)',
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderWidth': 2,
                'fill': True
            },
            {
                'label': 'Suhu Maksimum Rata-Rata',
                'data': suhu_maks['suhumaks'].round(2).tolist(),
                'borderColor': 'rgba(75, 192, 192, 1)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderWidth': 2,
                'fill': True
            },
            {
                'label': 'Suhu Minimum Rata-Rata',
                'data': suhu_min['suhumin'].round(2).tolist(),
                'borderColor': 'rgba(153, 102, 255, 1)',
                'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                'borderWidth': 2,
                'fill': True
            },
            {
                'label': 'Suhu Minimum Absolut',
                'data': suhu_min_abs['suhumin'].round(2).tolist(),
                'borderColor': 'rgba(255, 159, 64, 1)',
                'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                'borderWidth': 2,
                'fill': True
            }
        ]
    }
    
    return data2
