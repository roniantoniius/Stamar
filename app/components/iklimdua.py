import calendar
import pandas as pd
from app.models import DataFklim
from app.components.windrose import get_range

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
    
    # Menghitung rata-rata sinar matahari per bulan
    sinar_matahari_rata_rata = df_year.groupby('tahun')['sinarmatahari'].mean().reset_index()
    
    data = {
        'labels': sinar_matahari_rata_rata['tahun'].astype(str).tolist(),
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
    
    # Menghitung akumulasi curah hujan per bulan
    curah_hujan_rata_rata = df_year.groupby('tahun')['curahhujan'].sum().reset_index()
    
    # Menggabungkan data untuk dikirim dalam format JSON
    data = {
        'labels': curah_hujan_rata_rata['tahun'].astype(str).tolist(),
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
    
    # Menghitung maksimum curah hujan per bulan
    curah_hujan_maksimum = df_year.groupby('tahun')['curahhujan'].max().reset_index()

    # Menggabungkan data untuk dikirim dalam format JSON
    data = {
        'labels': curah_hujan_maksimum['tahun'].astype(str).tolist(),
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

def prepare_sinar_matahari_bulan(tahun=None, bulan=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])
    
    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    df_filtered = df[(df['tahun'].isin(tahun_range)) & (df['bulan'].isin(bulan_range))]
    df_filtered = df_filtered[df_filtered['sinarmatahari'] != 0]
    df_filtered['bulan'] = df_filtered['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    sinar_matahari_rata_rata = df_filtered.groupby('bulan')['sinarmatahari'].mean().reset_index()
    
    months = [calendar.month_abbr[i] for i in bulan_range]
    sinar_matahari_rata_rata['bulan'] = pd.Categorical(sinar_matahari_rata_rata['bulan'], categories=months, ordered=True)
    sinar_matahari_rata_rata.sort_values('bulan', inplace=True)

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

def akumulasi_curah_hujan_bulan(tahun=None, bulan=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])
    
    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    df_filtered = df[(df['tahun'].isin(tahun_range)) & (df['bulan'].isin(bulan_range))]
    df_filtered = df_filtered[df_filtered['curahhujan'] != 0]
    df_filtered['bulan'] = df_filtered['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    curah_hujan_rata_rata = df_filtered.groupby('bulan')['curahhujan'].sum().reset_index()
    
    months = [calendar.month_abbr[i] for i in bulan_range]
    curah_hujan_rata_rata['bulan'] = pd.Categorical(curah_hujan_rata_rata['bulan'], categories=months, ordered=True)
    curah_hujan_rata_rata.sort_values('bulan', inplace=True)

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

def curah_hujan_maksimum_bulan(tahun=None, bulan=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])
    
    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    df_filtered = df[(df['tahun'].isin(tahun_range)) & (df['bulan'].isin(bulan_range))]
    df_filtered['bulan'] = df_filtered['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    curah_hujan_maksimum = df_filtered.groupby('bulan')['curahhujan'].max().reset_index()
    
    months = [calendar.month_abbr[i] for i in bulan_range]
    curah_hujan_maksimum['bulan'] = pd.Categorical(curah_hujan_maksimum['bulan'], categories=months, ordered=True)
    curah_hujan_maksimum.sort_values('bulan', inplace=True)

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