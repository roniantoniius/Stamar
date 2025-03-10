import calendar
import pandas as pd
from app.models import DataFklim
from app.components.windrose import get_range

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
        if len(tahun) == 1:
            tahun_range = list(tahun)
        elif len(tahun) == 2:
            tahun_range = list(range(int(tahun[0]), int(tahun[1]) + 1))
        else:
            raise ValueError("Input tahun harus berupa satu tahun atau dua tahun")
    else:
        raise ValueError("Input tahun harus berupa string, list, atau tuple")

    # Memilih data sesuai tahun yang dipilih
    df_year = pd.concat([df[df['tahun'] == t] for t in tahun_range])
    df_year = df_year[(df_year['suhurata'] != 0) & (df_year['suhumaks'] != 0) & (df_year['suhumin'] != 0)]
    
    # Menghitung statistik suhu per bulan
    suhu_rata_rata = df_year.groupby('tahun')['suhurata'].mean().reset_index()
    suhu_maks_abs = df_year.groupby('tahun')['suhumaks'].max().reset_index()
    suhu_maks = df_year.groupby('tahun')['suhumaks'].mean().reset_index()
    suhu_min = df_year.groupby('tahun')['suhumin'].mean().reset_index()
    suhu_min_abs = df_year.groupby('tahun')['suhumin'].min().reset_index()


    # Menggabungkan data untuk dikirim dalam format JSON
    data = {
        'labels': suhu_rata_rata['tahun'].astype(str).tolist(),
        'datasets': [
            {
                'label': 'Suhu Rata-Rata',
                'data': suhu_rata_rata['suhurata'].round(2).tolist(),
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Suhu Maksimum Absolut',
                'data': suhu_maks_abs['suhumaks'].round(2).tolist(),
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Suhu Maksimum Rata-Rata',
                'data': suhu_maks['suhumaks'].round(2).tolist(),
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Suhu Minimum Rata-Rata',
                'data': suhu_min['suhumin'].round(2).tolist(),
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Suhu Minimum Absolut',
                'data': suhu_min_abs['suhumin'].round(2).tolist(),
                'borderColor': 'rgba(255, 159, 64, 1)',
                'borderWidth': 4,
                'fill': False
            }
        ]
    }
    
    return data

def prepare_kelembapan_data(tahun=None, session=None):
    # Mendapatkan data dari database
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])
    
    # Mengonversi tahun ke list yang dapat diolah
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
        raise ValueError("Input tahun harus berupa string, list, atau tuple")

    # Memilih data sesuai tahun yang dipilih
    df_year = pd.concat([df[df['tahun'] == t] for t in tahun_range])
    df_year = df_year[(df_year['kelembapanrata'] != 0) & (df_year['kelembapanmaks'] != 0) & (df_year['kelembapanmin'] != 0)]
    
    # Menghitung statistik kelembapan per bulan
    kelembapan_rata_rata = df_year.groupby('tahun')['kelembapanrata'].mean().reset_index()
    kelembapan_maks = df_year.groupby('tahun')['kelembapanmaks'].mean().reset_index()
    kelembapan_min = df_year.groupby('tahun')['kelembapanmin'].mean().reset_index()

    data = {
        'labels': kelembapan_rata_rata['tahun'].astype(str).tolist(),
        'datasets': [
            {
                'label': 'Kelembapan Rata-Rata',
                'data': kelembapan_rata_rata['kelembapanrata'].round(2).tolist(),
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Kelembapan Maksimum',
                'data': kelembapan_maks['kelembapanmaks'].round(2).tolist(),
                'borderColor': 'rgba(255, 159, 64, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Kelembapan Minimum',
                'data': kelembapan_min['kelembapanmin'].round(2).tolist(),
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 4,
                'fill': False
            },
        ]
    }
    
    return data

def prepare_tekanan_data(tahun=None, session=None):
    # Mengambil data dari database
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

    # Memproses input tahun
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
        raise ValueError("Input tahun harus berupa string, list, atau tuple")

    # Memilih data sesuai tahun
    df_year = pd.concat([df[df['tahun'] == t] for t in tahun_range])
    df_year = df_year[df_year['tekananudara'] != 0]

    # Menghitung statistik tekanan per bulan
    tekanan_rata_rata = df_year.groupby('tahun')['tekananudara'].mean().reset_index()
    tekanan_maks = df_year.groupby('tahun')['tekananudara'].max().reset_index()
    tekanan_min = df_year.groupby('tahun')['tekananudara'].min().reset_index()

    data = {
        'labels': tekanan_rata_rata['tahun'].astype(str).tolist(),
        'datasets': [
            {
                'label': 'Tekanan Rata-Rata',
                'data': tekanan_rata_rata['tekananudara'].round(2).tolist(),
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Tekanan Maksimum',
                'data': tekanan_maks['tekananudara'].round(2).tolist(),
                'borderColor': 'rgba(255, 159, 64, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Tekanan Minimum',
                'data': tekanan_min['tekananudara'].round(2).tolist(),
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 4,
                'fill': False
            },
        ]
    }

    return data

def prepare_suhu_bulan(tahun=None, bulan=None, session=None):
    # Mendapatkan data dari database
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])
    
    # Menggunakan get_range untuk tahun dan bulan
    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    # Memfilter data berdasarkan tahun dan bulan
    df_filtered = df[(df['tahun'].isin(tahun_range)) & (df['bulan'].isin(bulan_range))]
    df_filtered = df_filtered[(df_filtered['suhurata'] != 0) & 
                            (df_filtered['suhumaks'] != 0) & 
                            (df_filtered['suhumin'] != 0)]
    
    # Mengonversi nomor bulan ke nama bulan
    df_filtered['bulan'] = df_filtered['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    # Menghitung statistik suhu per bulan
    suhu_rata_rata = df_filtered.groupby('bulan')['suhurata'].mean().reset_index()
    suhu_maks_abs = df_filtered.groupby('bulan')['suhumaks'].max().reset_index()
    suhu_maks = df_filtered.groupby('bulan')['suhumaks'].mean().reset_index()
    suhu_min = df_filtered.groupby('bulan')['suhumin'].mean().reset_index()
    suhu_min_abs = df_filtered.groupby('bulan')['suhumin'].min().reset_index()
    
    # Urutkan berdasarkan bulan yang dipilih
    months = [calendar.month_abbr[i] for i in bulan_range]
    for df in [suhu_rata_rata, suhu_maks_abs, suhu_maks, suhu_min, suhu_min_abs]:
        df['bulan'] = pd.Categorical(df['bulan'], categories=months, ordered=True)
        df.sort_values('bulan', inplace=True)

    # Menggabungkan data untuk dikirim dalam format JSON
    data = {
        'labels': suhu_rata_rata['bulan'].tolist(),
        'datasets': [
            {
                'label': 'Suhu Rata-Rata',
                'data': suhu_rata_rata['suhurata'].round(2).tolist(),
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Suhu Maksimum Absolut',
                'data': suhu_maks_abs['suhumaks'].round(2).tolist(),
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Suhu Maksimum Rata-Rata',
                'data': suhu_maks['suhumaks'].round(2).tolist(),
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Suhu Minimum Rata-Rata',
                'data': suhu_min['suhumin'].round(2).tolist(),
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Suhu Minimum Absolut',
                'data': suhu_min_abs['suhumin'].round(2).tolist(),
                'borderColor': 'rgba(255, 159, 64, 1)',
                'borderWidth': 4,
                'fill': False
            }
        ]
    }
    
    return data

def prepare_kelembapan_bulan(tahun=None, bulan=None, session=None):
    # Mendapatkan data dari database
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])
    
    # Menggunakan get_range untuk tahun dan bulan
    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    # Memfilter data berdasarkan tahun dan bulan
    df_filtered = df[(df['tahun'].isin(tahun_range)) & (df['bulan'].isin(bulan_range))]
    df_filtered = df_filtered[(df_filtered['kelembapanrata'] != 0) & 
                              (df_filtered['kelembapanmaks'] != 0) & 
                              (df_filtered['kelembapanmin'] != 0)]
    
    # Mengonversi nomor bulan ke nama bulan
    df_filtered['bulan'] = df_filtered['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    # Menghitung statistik kelembapan per bulan
    kelembapan_rata_rata = df_filtered.groupby('bulan')['kelembapanrata'].mean().reset_index()
    kelembapan_maks = df_filtered.groupby('bulan')['kelembapanmaks'].mean().reset_index()
    kelembapan_min = df_filtered.groupby('bulan')['kelembapanmin'].mean().reset_index()
    
    # Urutkan berdasarkan bulan yang dipilih
    months = [calendar.month_abbr[i] for i in bulan_range]
    for df in [kelembapan_rata_rata, kelembapan_maks, kelembapan_min]:
        df['bulan'] = pd.Categorical(df['bulan'], categories=months, ordered=True)
        df.sort_values('bulan', inplace=True)

    # Menggabungkan data untuk dikirim dalam format JSON
    data = {
        'labels': kelembapan_rata_rata['bulan'].tolist(),
        'datasets': [
            {
                'label': 'Kelembapan Rata-Rata',
                'data': kelembapan_rata_rata['kelembapanrata'].round(2).tolist(),
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Kelembapan Maksimum',
                'data': kelembapan_maks['kelembapanmaks'].round(2).tolist(),
                'borderColor': 'rgba(255, 159, 64, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Kelembapan Minimum',
                'data': kelembapan_min['kelembapanmin'].round(2).tolist(),
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 4,
                'fill': False
            },
        ]
    }
    
    return data

def prepare_tekanan_bulan(tahun=None, bulan=None, session=None):
    # Mengambil data dari database
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

    # Menggunakan get_range untuk tahun dan bulan
    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    # Memfilter data berdasarkan tahun dan bulan
    df_filtered = df[(df['tahun'].isin(tahun_range)) & (df['bulan'].isin(bulan_range))]
    df_filtered = df_filtered[df_filtered['tekananudara'] != 0]
    
    # Mengonversi nomor bulan ke nama bulan
    df_filtered['bulan'] = df_filtered['bulan'].apply(lambda x: calendar.month_abbr[x])

    # Menghitung statistik tekanan per bulan
    tekanan_rata_rata = df_filtered.groupby('bulan')['tekananudara'].mean().reset_index()
    tekanan_maks = df_filtered.groupby('bulan')['tekananudara'].max().reset_index()
    tekanan_min = df_filtered.groupby('bulan')['tekananudara'].min().reset_index()

    # Urutkan berdasarkan bulan yang dipilih
    months = [calendar.month_abbr[i] for i in bulan_range]
    for df in [tekanan_rata_rata, tekanan_maks, tekanan_min]:
        df['bulan'] = pd.Categorical(df['bulan'], categories=months, ordered=True)
        df.sort_values('bulan', inplace=True)

    # Menyiapkan data untuk format JSON
    data = {
        'labels': tekanan_rata_rata['bulan'].tolist(),
        'datasets': [
            {
                'label': 'Tekanan Rata-Rata',
                'data': tekanan_rata_rata['tekananudara'].round(2).tolist(),
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Tekanan Maksimum',
                'data': tekanan_maks['tekananudara'].round(2).tolist(),
                'borderColor': 'rgba(255, 159, 64, 1)',
                'borderWidth': 4,
                'fill': False
            },
            {
                'label': 'Tekanan Minimum',
                'data': tekanan_min['tekananudara'].round(2).tolist(),
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 4,
                'fill': False
            },
        ]
    }

    return data