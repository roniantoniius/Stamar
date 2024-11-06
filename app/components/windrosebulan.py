import calendar
import pandas as pd
from app.models import DataFklim

def get_range(input_value, default_range):
    if input_value is None:
        return default_range
    elif isinstance(input_value, (int, str)):
        return [int(input_value)]
    elif isinstance(input_value, (list, tuple)):
        if len(input_value) == 1:
            return [int(input_value[0])]
        elif len(input_value) == 2:
            return list(range(int(input_value[0]), int(input_value[-1]) + 1))
        else:
            return [int(x) for x in input_value]
    else:
        return ValueError("Input harus berupa integer, string, list, atau tuple")

def generate_wind_rose_bulan(tahun=None, bulan=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    df_filtered = df[(df['tahun'].isin(tahun_range)) & (df['bulan'].isin(bulan_range))]
    df_filtered = df_filtered[df_filtered['anginkecmaks'] != 0]

    wind_rose_data = {}
    for month in bulan_range:
        monthly_data = df_filtered[df_filtered['bulan'] == month]
        if monthly_data.empty:
            continue

        month_avg_data = monthly_data.groupby('anginarah')['anginkecmaks'].mean().reset_index()

        colors = [
            'rgba(255, 0, 0, 0.6)' if speed <= 5 else
            'rgba(255, 165, 0, 0.6)' if speed <= 10 else
            'rgba(255, 255, 0, 0.6)' if speed <= 15 else
            'rgba(144, 238, 144, 0.6)' if speed <= 20 else
            'rgba(0, 128, 0, 0.6)' if speed <= 25 else
            '#12ffd3'
            for speed in month_avg_data['anginkecmaks']
        ]

        wind_rose_data[calendar.month_abbr[month]] = {
            'datasets': [{
                'label': f'Average Wind Speed ({calendar.month_abbr[month]})',
                'data': month_avg_data['anginkecmaks'].tolist(),
                'backgroundColor': colors
            }],
            'labels': month_avg_data['anginarah'].tolist()
        }

    return wind_rose_data

def generate_kecepatan_angin_bulan(tahun=None, bulan=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    # Filter data by year and month
    df_year = pd.concat([df[(df['tahun'] == t) & (df['bulan'] == m)] for t in tahun_range for m in bulan_range])
    df_year = df_year[df_year['anginkecmaks'] != 0]

    df_year