import pandas as pd
from app.models import DataFklim

def categorize_cuaca(cuaca):
    cuaca = cuaca.lower()
    if 'ts' in cuaca and 'ra' in cuaca:
        return 'TS/RA: Hujan Petir'
    elif 'ra' in cuaca and 'ts' not in cuaca:
        return 'RA: Hujan'
    elif 'ts' in cuaca and 'ra' not in cuaca:
        return 'TS: Petir'
    elif 'haze' in cuaca:
        return 'Haze: Udara Kabur'
    elif 'drizle' in cuaca:
        return 'Drizle: Gerimis'
    elif cuaca == 'nil' or cuaca == 'nill':
        return 'NIL: Cerah / Belum ada Cuaca'
    else:
        return 'NIL: Cerah / Belum ada Cuaca'

def persentase_cuaca_data(tahun=None, session=None):
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
    df_filtered = pd.concat([df[df['tahun'] == t] for t in tahun_range])
    df_filtered['cuaca_categorized'] = df_filtered['cuaca'].apply(categorize_cuaca)

    # Menghitung frekuensi setiap kategori cuaca
    cuaca_counts = df_filtered['cuaca_categorized'].value_counts(normalize=True) * 100
    cuaca_counts = cuaca_counts.reset_index()
    cuaca_counts.columns = ['kategori', 'persentase']

    # Mengonversi data menjadi format JSON untuk visualisasi
    data = {
        'labels': cuaca_counts['kategori'].tolist(),
        'datasets': [
            {
                'data': cuaca_counts['persentase'].tolist(),
                'backgroundColor': [
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(201, 203, 207, 0.6)',
                ],
                'borderColor': [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(201, 203, 207, 1)',
                ],
                'borderWidth': 1
            }
        ]
    }
    
    return data
