import calendar
import pandas as pd
from app.models import DataFklim

def prepare_sinar_matahari_data(tahun=None, session=None):
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
    df_year = df_year[df_year['sinarmatahari'] != 0]  # Pastikan nama kolom sesuai dengan database
    df_year['bulan'] = df_year['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    # Menghitung rata-rata sinar matahari per bulan
    sinar_matahari_rata_rata = df_year.groupby('bulan')['sinarmatahari'].mean().reset_index()
    
    # Urutkan berdasarkan bulan
    months = calendar.month_abbr[1:13]
    sinar_matahari_rata_rata['bulan'] = pd.Categorical(sinar_matahari_rata_rata['bulan'], categories=months, ordered=True)
    sinar_matahari_rata_rata.sort_values('bulan', inplace=True)

    # Menggabungkan data untuk dikirim dalam format JSON
    data = {
        'labels': sinar_matahari_rata_rata['bulan'].tolist(),
        'datasets': [
            {
                'label': 'Rata-rata Penyinaran Matahari',
                'data': sinar_matahari_rata_rata['sinarmatahari'].round(2).tolist(),
                'backgroundColor': 'rgba(255, 193, 7, 0.6)',
                'borderColor': 'rgba(255, 140, 0, 1)',
                'borderWidth': 3
            }
        ]
    }
    
    return data

def akumulasi_curah_hujan(tahun=None, session=None):
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
    df_year = df_year[df_year['curahhujan'] != 0]  # Pastikan nama kolom sesuai dengan database
    df_year['bulan'] = df_year['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    # Menghitung akumulasi curah hujan per bulan
    curah_hujan_rata_rata = df_year.groupby('bulan')['curahhujan'].sum().reset_index()
    
    # Urutkan berdasarkan bulan
    months = calendar.month_abbr[1:13]
    curah_hujan_rata_rata['bulan'] = pd.Categorical(curah_hujan_rata_rata['bulan'], categories=months, ordered=True)
    curah_hujan_rata_rata.sort_values('bulan', inplace=True)

    # Menggabungkan data untuk dikirim dalam format JSON
    data = {
        'labels': curah_hujan_rata_rata['bulan'].tolist(),
        'datasets': [
            {
                'label': 'Akumulasi Curah Hujan',
                'data': curah_hujan_rata_rata['curahhujan'].round(2).tolist(),
                'backgroundColor': 'rgba(153, 102, 255, 0.6)',
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 3
            }
        ]
    }
    
    return data

def curah_hujan_maksimum(tahun=None, session=None):
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
    df_year['bulan'] = df_year['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    # Menghitung maksimum curah hujan per bulan
    curah_hujan_maksimum = df_year.groupby('bulan')['curahhujan'].max().reset_index()
    
    # Urutkan berdasarkan bulan
    months = calendar.month_abbr[1:13]
    curah_hujan_maksimum['bulan'] = pd.Categorical(curah_hujan_maksimum['bulan'], categories=months, ordered=True)
    curah_hujan_maksimum.sort_values('bulan', inplace=True)

    # Menggabungkan data untuk dikirim dalam format JSON
    data = {
        'labels': curah_hujan_maksimum['bulan'].tolist(),
        'datasets': [
            {
                'label': 'Maksimum Curah Hujan',
                'data': curah_hujan_maksimum['curahhujan'].round(2).tolist(),
                'backgroundColor': 'rgba(75, 192, 192, 0.6)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 3
            }
        ]
    }
    
    return data
