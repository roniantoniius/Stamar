import calendar
import pandas as pd
from app.models import DataFklim

def wind_rose(tahun=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

    # Handle year input as you already have
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
    
    # Change this part to group by year instead of month
    for year in tahun_range:
        yearly_data = df_filtered[df_filtered['tahun'] == year]
        if yearly_data.empty:
            continue

        year_avg_data = yearly_data.groupby('anginarah')['anginkecmaks'].mean().reset_index()

        # Set colors for different wind speeds
        colors = [
            'rgba(255, 0, 0, 0.6)' if speed <= 5 else
            'rgba(255, 165, 0, 0.6)' if speed <= 10 else
            'rgba(255, 255, 0, 0.6)' if speed <= 15 else
            'rgba(144, 238, 144, 0.6)' if speed <= 20 else
            'rgba(0, 128, 0, 0.6)' if speed <= 25 else
            '#12ffd3'
            for speed in year_avg_data['anginkecmaks']
        ]

        wind_rose_data[year] = {
            'datasets': [{
                'label': f'Kecepatan Angin Rata-rata ({year})',
                'data': year_avg_data['anginkecmaks'].tolist(),
                'backgroundColor': colors
            }],
            'labels': year_avg_data['anginarah'].tolist()
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
    
    # df_year['bulan'] = df_year['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    kecepatan_angin_rata_rata = df_year.groupby('tahun')['anginkecmaks'].mean().reset_index()
    
    # months = calendar.month_abbr[1:13]
    # kecepatan_angin_rata_rata['bulan'] = pd.Categorical(kecepatan_angin_rata_rata['bulan'], categories=months, ordered=True)
    # kecepatan_angin_rata_rata = kecepatan_angin_rata_rata.sort_values('bulan')
    
    # Prepare data for Chart.js
    data = {
        'labels': kecepatan_angin_rata_rata['tahun'].astype(str).tolist(),
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

def chart_kecepatan_angin_bulan(tahun=None, bulan=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

    tahun_range = get_range(tahun, df['tahun'].unique())
    bulan_range = get_range(bulan, range(1, 13))

    df_filtered = df[(df['tahun'].isin(tahun_range)) & (df['bulan'].isin(bulan_range))]
    df_filtered = df_filtered[df_filtered['anginkecmaks'] != 0]
    
    df_filtered['bulan'] = df_filtered['bulan'].apply(lambda x: calendar.month_abbr[x])
    
    kecepatan_angin_rata_rata = df_filtered.groupby('bulan')['anginkecmaks'].mean().reset_index()
    
    months = [calendar.month_abbr[i] for i in bulan_range]
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