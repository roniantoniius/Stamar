from app.exts import db
from flask import Blueprint, render_template, jsonify
from app.components.windrose import chart_kecepatan_angin_tahun, wind_rose
from app.components.iklimsatu import prepare_suhu_data, prepare_kelembapan_data, prepare_tekanan_data
from app.components.iklimdua import prepare_sinar_matahari_data, akumulasi_curah_hujan, curah_hujan_maksimum
from app.components.iklimtiga import persentase_cuaca_data

tahunan_bp = Blueprint('tahunan', __name__)

@tahunan_bp.route('/tahunan')
def tahunan():
    session = db.session
    tahun_range = ['1991', '2020']
    
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

    return render_template('tahunan.html',
                           wind_rose_data=wind_rose_data,
                           kecepatan_angin_data=kecepatan_angin_data,
                           suhu_data=suhu_data,
                           kelembapan_data=kelembapan_data,
                           tekanan_data=tekanan_data,
                           matahari_data=matahari_data,
                           akumulasi_hujan=akumulasi_hujan,
                           maks_hujan=maks_hujan,
                           cuaca_data=cuaca_data)
