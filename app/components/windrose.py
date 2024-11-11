import calendar
import pandas as pd
from app.models import DataFklim

def classify_speed(speed):
    if speed <= 5:
        return "0-5 m/s"
    elif speed <= 10:
        return "5-10 m/s"
    elif speed <= 15:
        return "10-15 m/s"
    elif speed <= 20:
        return "15-20 m/s"
    elif speed <= 25:
        return "20-25 m/s"
    else:
        return "25+ m/s"
    
def convert_to_direction(degrees):
    # Normalize degrees to fall within 0-360 range
    degrees = degrees % 360
    
    # Define the 8 cardinal and intercardinal directions
    if 0 <= degrees < 22.5 or 337.5 <= degrees < 360:
        return 'N'   # North
    elif 22.5 <= degrees < 67.5:
        return 'NE'  # North-East
    elif 67.5 <= degrees < 112.5:
        return 'E'   # East
    elif 112.5 <= degrees < 157.5:
        return 'SE'  # South-East
    elif 157.5 <= degrees < 202.5:
        return 'S'   # South
    elif 202.5 <= degrees < 247.5:
        return 'SW'  # South-West
    elif 247.5 <= degrees < 292.5:
        return 'W'   # West
    elif 292.5 <= degrees < 337.5:
        return 'NW'  # North-West
    else:
        return 'N'  # Default to North if something unexpected occurs

def wind_rose(tahun=None, session=None):
    df = session.query(DataFklim).all()
    df = pd.DataFrame([data.to_dict() for data in df])

    # Filter by year as previously
    if tahun is None:
        tahun_range = df['tahun'].unique()
    elif isinstance(tahun, (str, list, tuple)):
        tahun_range = [int(tahun)] if isinstance(tahun, str) else list(range(int(tahun[0]), int(tahun[1]) + 1))
    else:
        raise ValueError("Input tahun harus berupa string, list, atau tuple")

    df_filtered = df[df['tahun'].isin(tahun_range)]
    df_filtered = df_filtered[df_filtered['anginkecmaks'] != 0]
    
    wind_rose_data = {}

    # Initialize the list of all 8 directions
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    for year in tahun_range:
        yearly_data = df_filtered[df_filtered['tahun'] == year]
        if yearly_data.empty:
            continue

        yearly_data['direction'] = yearly_data['anginarah'].apply(convert_to_direction)
        yearly_data['speed_category'] = yearly_data['anginkecmaks'].apply(classify_speed)

        # Initialize wind data with 0s for each direction and speed category
        wind_data = {direction: {category: 0 for category in ["0-5 m/s", "5-10 m/s", "10-15 m/s", "15-20 m/s", "20-25 m/s", "25+ m/s"]}
                     for direction in directions}

        # Group by direction and speed category, then fill in the wind_data
        for (direction, speed_category), count in (
            yearly_data.groupby(['direction', 'speed_category']).size().items()):
            wind_data[direction][speed_category] = count

        wind_rose_data[year] = wind_data

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

        monthly_data['direction'] = monthly_data['anginarah'].apply(convert_to_direction)
        monthly_data['speed_category'] = monthly_data['anginkecmaks'].apply(classify_speed)

        # Initialize wind data with 0s for each direction and speed category
        wind_data = {direction: {category: 0 for category in ["0-5 m/s", "5-10 m/s", "10-15 m/s", "15-20 m/s", "20-25 m/s", "25+ m/s"]}
                     for direction in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']}

        # Group by direction and speed category, then fill in the wind_data
        for (direction, speed_category), count in (
            monthly_data.groupby(['direction', 'speed_category']).size().items()):
            wind_data[direction][speed_category] = count

        wind_rose_data[calendar.month_abbr[month]] = wind_data

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