import calendar
import pandas as pd
import plotly.express as px
from app.models import DataFklim


def wind_rose(tahun=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

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

    df_filtered = df[df['tahun'].isin(tahun_range)]
    df_filtered = df_filtered[df_filtered['anginkecmaks'] != 0]

    wind_rose_data = {}
    for month in range(1, 13):
        monthly_data = df_filtered[df_filtered['bulan'] == month]
        if monthly_data.empty:
            continue

        month_avg_data = monthly_data.groupby('anginarah')['anginkecmaks'].mean().reset_index()

        colors = [
            'rgba(255, 0, 0, 0.6)' if speed <= 5 else  # Merah
            'rgba(255, 165, 0, 0.6)' if speed <= 10 else  # Oranye
            'rgba(255, 255, 0, 0.6)' if speed <= 15 else  # Kuning
            'rgba(144, 238, 144, 0.6)' if speed <= 20 else  # Hijau Terang
            'rgba(0, 128, 0, 0.6)' if speed <= 25 else  # Hijau Tua
            'rgba(0, 0, 255, 0.6)'  # Biru
            for speed in month_avg_data['anginkecmaks']
        ]

        wind_rose_data[calendar.month_abbr[month]] = {
            'datasets': [{
                'label': f'Kecepatan Angin Rata-rata ({calendar.month_abbr[month]})',
                'data': month_avg_data['anginkecmaks'].tolist(),
                'backgroundColor': colors
            }],
            'labels': month_avg_data['anginarah'].tolist()
        }

    return wind_rose_data

def chart_kecepatan_angin_tahun(tahun=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])  

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

    df_year = pd.concat([df[df['tahun'] == t] for t in tahun_range])
    df_year = df_year[df_year['anginkecmaks'] != 0]
    
    df_year['bulan'] = df_year['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    kecepatan_angin_rata_rata = df_year.groupby('bulan')['anginkecmaks'].mean().reset_index()
    
    months = calendar.month_abbr[1:13]
    kecepatan_angin_rata_rata['bulan'] = pd.Categorical(kecepatan_angin_rata_rata['bulan'], categories=months, ordered=True)
    kecepatan_angin_rata_rata = kecepatan_angin_rata_rata.sort_values('bulan')
    
    # Prepare data for Chart.js
    data = {
        'labels': kecepatan_angin_rata_rata['bulan'].tolist(),
        'datasets': [{
            'label': 'Rata-rata Kecepatan Angin Maksimum',
            'data': kecepatan_angin_rata_rata['anginkecmaks'].round(2).tolist(),
            'borderColor': 'rgba(75, 192, 192, 1)',
            'backgroundColor': 'rgba(75, 192, 192, 0.4)',
            'borderWidth': 4,
            'fill': True,
        }]
    }
    
    return data