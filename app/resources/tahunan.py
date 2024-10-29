from app.exts import db
from app.models import DataFklim
from flask import Blueprint, render_template
from app.components.windrose import visualisasi_windrose_tahun, chart_kecepatan_angin_tahun

tahunan_bp = Blueprint('tahunan', __name__)

@tahunan_bp.route('/tahunan')
def tahunan():
    session = db.session
    tahun_range = ['1991', '2020']
    windrose_plots = visualisasi_windrose_tahun(tahun=tahun_range, session=session)
    kecepatan_plot = chart_kecepatan_angin_tahun(tahun=tahun_range, session=session)

    return render_template('tahunan.html', windrose_plots=windrose_plots, kecepatan_plot=kecepatan_plot)
