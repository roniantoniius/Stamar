from app import db
from app.models import DataFklim

def get_last_row():
    """Mengembalikan baris terakhir dari tabel DataFklim"""
    last_row = db.session.query(DataFklim).order_by(DataFklim.id.desc()).first()
    return last_row.to_dict() if last_row else "No data found"