from app.exts import db
from calendar import month_name
from app.components.kpi import kpi_iklim_bulan
from flask import Blueprint, render_template, request
from app.components.iklimtiga import persentase_cuaca_data_bulan
from app.components.windrose import generate_wind_rose_bulan, chart_kecepatan_angin_bulan
from app.components.iklimsatu import prepare_suhu_bulan, prepare_tekanan_bulan, prepare_kelembapan_bulan
from app.components.iklimdua import prepare_sinar_matahari_bulan, curah_hujan_maksimum_bulan, akumulasi_curah_hujan_bulan

bulanan_bp = Blueprint('bulanan', __name__)

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

def get_month_name(month_number):
    return month_name[month_number]

@bulanan_bp.route('/bulanan')
def bulanan():
    session = db.session
    tahun_awal = request.args.get('tahun_awal')
    tahun_akhir = request.args.get('tahun_akhir')
    bulan_awal = request.args.get('bulan_awal')
    bulan_akhir = request.args.get('bulan_akhir')

    try:
        tahun_awal = int(tahun_awal)
        tahun_range = [tahun_awal]
        if tahun_akhir:
            tahun_akhir = int(tahun_akhir)
            tahun_range = list(range(tahun_awal, tahun_akhir + 1))

        bulan_awal = int(bulan_awal)
        bulan_range = [bulan_awal]
        if bulan_akhir:
            bulan_akhir = int(bulan_akhir)
            bulan_range = list(range(bulan_awal, bulan_akhir + 1))

    except ValueError:
        return "Invalid year or month input", 400
    
    if len(tahun_range) == 1:
        year_part = f'Tahun {tahun_range[0]}'
    else:
        if tahun_range[-1] - tahun_range[0] >= 29:
            year_part = f'Periode {tahun_range[0]} - {tahun_range[-1]}'
        else:
            year_part = f'Periode {tahun_range[0]} - {tahun_range[-1]}'

    if len(bulan_range) == 1:
        month_part = f'Bulan {get_month_name(bulan_range[0])}'
    else:
        month_part = f'Bulan {get_month_name(bulan_range[0])} - {get_month_name(bulan_range[-1])}'

    if len(tahun_range) == 1 or tahun_range[-1] - tahun_range[0] < 29:
        title = f'Data Iklim {month_part} {year_part}'
    else:
        title = f'Data Normal Iklim {month_part} {year_part}'

    wind_rose_data_bulan = generate_wind_rose_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    kecepatan_angin_bulan = chart_kecepatan_angin_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    suhu_data_bulan = prepare_suhu_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    tekanan_data_bulan = prepare_tekanan_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    kelembapan_data_bulan = prepare_kelembapan_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    sinar_matahari_data_bulan = prepare_sinar_matahari_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    hujan_maksimum_data_bulan = curah_hujan_maksimum_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    hujan_akumulasi_data_bulan = akumulasi_curah_hujan_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    cuaca_data_bulan = persentase_cuaca_data_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    kpi_data_bulan = kpi_iklim_bulan(tahun=tahun_range, bulan=bulan_range, session=session)
    

    return render_template('bulanan.html',
                            title=title,
                            add_unit=add_unit,
                            wind_rose_bulan=wind_rose_data_bulan,
                            kecepatan_bulan=kecepatan_angin_bulan,
                            suhu_bulan = suhu_data_bulan,
                            tekanan_bulan = tekanan_data_bulan,
                            kelembapan_bulan = kelembapan_data_bulan,
                            matahari_bulan = sinar_matahari_data_bulan,
                            hujan_maksimum_bulan = hujan_maksimum_data_bulan,
                            hujan_akumulasi_bulan = hujan_akumulasi_data_bulan,
                            cuaca_bulan = cuaca_data_bulan,
                            kpi_bulan = kpi_data_bulan)