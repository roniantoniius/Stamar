from app.exts import db
from flask import Blueprint, render_template, request

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
    
@bulanan_bp.route('/bulanan')
def bulanan():
    return render_template('bulanan.html', title='Data Iklim Bulanan')