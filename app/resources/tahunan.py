from app.exts import db
from flask import Blueprint, render_template, request
from app.components.windrose import chart_kecepatan_angin_tahun, wind_rose
from app.components.iklimsatu import prepare_suhu_data, prepare_kelembapan_data, prepare_tekanan_data
from app.components.iklimdua import prepare_sinar_matahari_data, akumulasi_curah_hujan, curah_hujan_maksimum
from app.components.iklimtiga import persentase_cuaca_data
from app.components.kpi import kpi_iklim

tahunan_bp = Blueprint('tahunan', __name__)


def add_unit(parameter, value):
    if 'Suhu' in parameter:
        return f"{value} °C"
    elif 'Curah Hujan' in parameter:
        return f"{value} mm"
    elif 'Tekanan Udara' in parameter:
        return f"{value} hPa"
    elif 'Kelembapan' in parameter:
        return f"{value}%"
    elif 'Kecepatan Angin' in parameter:
        return f"{value} m/s"
    else:
        return value

@tahunan_bp.route('/tahunan')
def tahunan():
    session = db.session
    tahun_awal = request.args.get('tahun_awal')
    tahun_akhir = request.args.get('tahun_akhir')

    try:
        tahun_awal = int(tahun_awal)
        if tahun_akhir:
            tahun_akhir = int(tahun_akhir)
            tahun_range = [tahun_awal, tahun_akhir]
        else:
            tahun_range = [tahun_awal]
    except ValueError:
        # Jika konversi gagal, kembalikan error atau default
        return "Tahun yang dimasukkan tidak valid", 400
    
    # Mengambil data untuk Chart.js
    wind_rose_data = wind_rose(tahun=tahun_range, session=session)
    kecepatan_angin_data = chart_kecepatan_angin_tahun(tahun=tahun_range, session=session)
    suhu_data = prepare_suhu_data(tahun=tahun_range, session=session)
    kelembapan_data = prepare_kelembapan_data(tahun=tahun_range, session=session)
    tekanan_data = prepare_tekanan_data(tahun=tahun_range, session=session)

    matahari_data = prepare_sinar_matahari_data(tahun=tahun_range, session=session)
    akumulasi_hujan = akumulasi_curah_hujan(tahun=tahun_range, session=session)
    maks_hujan = curah_hujan_maksimum(tahun=tahun_range, session=session)

    cuaca_data = persentase_cuaca_data(tahun=tahun_range, session=session)
    kpi_data = kpi_iklim(tahun=tahun_range, session=session)

    if len(tahun_range) == 1:
        title = f'Data Iklim Pada Tahun {tahun_range[0]}'
    elif len(tahun_range) > 1:
        if tahun_range[-1] - tahun_range[0] >= 29:
            title = f'Data Normal Iklim Periode {tahun_range[0]} - {tahun_range[-1]}'
        else:
            title = f'Data Iklim Tahunan Periode {tahun_range[0]} - {tahun_range[-1]}'

    return render_template('tahunan.html',
                           wind_rose_data=wind_rose_data,
                           kecepatan_angin_data=kecepatan_angin_data,
                           suhu_data=suhu_data,
                           kelembapan_data=kelembapan_data,
                           tekanan_data=tekanan_data,
                           matahari_data=matahari_data,
                           akumulasi_hujan=akumulasi_hujan,
                           maks_hujan=maks_hujan,
                           cuaca_data=cuaca_data,
                           kpi_data=kpi_data,
                           add_unit=add_unit,
                           title=title)
