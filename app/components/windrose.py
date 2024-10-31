import calendar
import pandas as pd
import plotly.express as px
from app.models import DataFklim

# def wind_rose(tahun=None, session=None):
#     # Load data from the database
#     df = session.query(DataFklim).all()
#     df = pd.DataFrame([data.to_dict() for data in df])

#     # Convert 'tahun' to an integer range based on input type
#     if tahun is None:
#         tahun_range = df['tahun'].unique()
#     elif isinstance(tahun, str):
#         tahun_range = [int(tahun)]
#     elif isinstance(tahun, list) or isinstance(tahun, tuple):
#         tahun_range = list(range(int(tahun[0]), int(tahun[1]) + 1))
#     else:
#         raise ValueError("Input tahun harus berupa string, list, atau tuple")

#     # Filter data by year range and exclude rows with zero wind speed
#     df_filtered = df[df['tahun'].isin(tahun_range)]
#     df_filtered = df_filtered[df_filtered['anginkecmaks'] != 0]

#     # Group by month and prepare data for each month
#     wind_rose_data = {}
#     for month in range(1, 13):
#         monthly_data = df_filtered[df_filtered['bulan'] == month]
#         if monthly_data.empty:
#             continue

#         # Aggregate by direction and calculate mean speed for each direction
#         month_avg_data = monthly_data.groupby('anginarah')['anginkecmaks'].mean().reset_index()

#         # Add data to the dictionary for each month
#         wind_rose_data[calendar.month_abbr[month]] = {
#             'labels': month_avg_data['anginarah'].tolist(),
#             'datasets': [{
#                 'label': f'Kecepatan Angin Rata-rata ({calendar.month_abbr[month]})',
#                 'data': month_avg_data['anginkecmaks'].tolist(),
#                 'backgroundColor': [
#                     'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 
#                     'rgba(255, 206, 86, 0.6)', 'rgba(75, 192, 192, 0.6)',
#                     'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)'
#                 ]
#             }]
#         }
#     return wind_rose_data

def wind_rose(tahun=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

    if tahun is None:
        tahun_range = df['tahun'].unique()
    elif isinstance(tahun, str):
        tahun_range = [int(tahun)]
    elif isinstance(tahun, list) or isinstance(tahun, tuple):
        tahun_range = list(range(int(tahun[0]), int(tahun[1]) + 1))
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
        tahun_range = list(range(int(tahun[0]), int(tahun[1]) + 1))
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