from app.exts import db
from flask import Blueprint, render_template, jsonify
from app.components.windrose import chart_kecepatan_angin_tahun
from app.components.iklimsatu import prepare_suhu_data

tahunan_bp = Blueprint('tahunan', __name__)

@tahunan_bp.route('/tahunan')
def tahunan():
    session = db.session
    tahun_range = ['1991', '2020']
    
    # Mengambil data untuk Chart.js
    kecepatan_angin_data = chart_kecepatan_angin_tahun(tahun=tahun_range, session=session)
    suhu_data = prepare_suhu_data(tahun=tahun_range, session=session)

    return render_template('tahunan.html', kecepatan_angin_data=kecepatan_angin_data, suhu_data=suhu_data)
