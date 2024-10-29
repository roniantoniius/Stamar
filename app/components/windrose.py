import calendar
import pandas as pd
import plotly.express as px
from app.models import DataFklim

def visualisasi_windrose_tahun(tahun=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

    if tahun is None:
        tahun_range = df['tahun'].unique()
    elif isinstance(tahun, str):
        tahun_range = [int(tahun)]
    elif isinstance(tahun, int):
        tahun_range = [tahun]
    elif isinstance(tahun, list) or isinstance(tahun, tuple):
        tahun_range = list(range(int(tahun[0]), int(tahun[1]) + 1))
    else:
        raise ValueError("Input tahun harus berupa integer, string, list, atau tuple.")

    df_filtered = df[df['tahun'].isin(tahun_range)]
    
    month_avg_data = df_filtered.groupby('bulan').agg(
        {'anginarah': lambda x: x.dropna().tolist(),
         'anginkecrata': lambda x: x[x > 0].mean()}
    ).reset_index()

    windrose_figures = []  # List untuk menyimpan visualisasi windrose

    for j in month_avg_data['bulan'].unique():
        df_windrose = month_avg_data[month_avg_data['bulan'] == j]

        if df_windrose['anginkecrata'].isna().all():
            continue

        directions = df_windrose['anginarah'].values[0]
        speeds = [df_windrose['anginkecrata'].values[0]] * len(directions)
        
        windrose_data = pd.DataFrame({
            'Arah Angin': directions,
            'Kecepatan Angin': speeds
        })
        
        fig = px.bar_polar(
            windrose_data,
            r="Kecepatan Angin",
            theta="Arah Angin",
            color="Kecepatan Angin",
            color_continuous_scale=['red', 'orange', 'yellow', 'lightgreen', 'darkgreen', 'blue'],
            range_color=[0, 25],
            labels={'r': 'Kecepatan Angin', 'theta': 'Arah Angin'},
            title=f'Bulan {calendar.month_name[j]} '
        )

        fig.update_traces(marker=dict(line=dict(color='orange', width=1)))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(range=[0, max(speeds) + 5], showticklabels=True),
                angularaxis=dict(direction="clockwise")
            )
        )

        # Simpan plotly figure sebagai HTML
        windrose_figures.append(fig.to_html(full_html=False))

    return windrose_figures  # Kembalikan list dari HTML visualisasi

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
    
    if len(tahun_range) == 1:
        title = f'Rata-rata Kecepatan Angin Maksimum Tahun {tahun_range[0]}'
    elif len(tahun_range) > 1:
        if tahun_range[-1] - tahun_range[0] >= 29:
            title = f'Data Normal Rata-rata Kecepatan Angin Maksimum Periode {tahun_range[0]} - {tahun_range[-1]}'
        else:
            title = f'Data Tahunan Rata-rata Kecepatan Angin Maksimum Periode {tahun_range[0]} - {tahun_range[-1]}'
    
    fig = px.line(
        kecepatan_angin_rata_rata,
        x='bulan',
        y='anginkecmaks',
        markers=True,
        title=title,
        labels={'bulan': 'Bulan', 'anginkecmaks': 'Kecepatan Angin Maksimum'}
    )
    
    fig.update_traces(text=kecepatan_angin_rata_rata['anginkecmaks'].round(2),
                      textposition='top center')

    fig.update_layout(
        xaxis=dict(title='Bulan'),
        yaxis=dict(title='Kecepatan Angin Maksimum'),
    )

    return fig.to_html(full_html=False)  # Kembalikan HTML visualisasi
