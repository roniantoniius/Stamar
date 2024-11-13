from sqlalchemy.sql import func
from app.exts import db

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)

	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

	def __init__(self, email, password):
		self.email = email
		self.password = password

class DataFklim(db.Model):
    __tablename__ = 'data_fklim'

    id = db.Column(db.Integer, primary_key=True)
    nosta = db.Column(db.Integer, nullable=True)
    namasta = db.Column(db.String, nullable=True)
    tahun = db.Column(db.Integer, nullable=False)
    bulan = db.Column(db.Integer, nullable=False)
    tgl = db.Column(db.Integer, nullable=False)
    suhu7 = db.Column(db.Float, nullable=True)
    suhu13 = db.Column(db.Float, nullable=True)
    suhu18 = db.Column(db.Float, nullable=True)
    suhurata = db.Column(db.Float, nullable=True)
    suhumaks = db.Column(db.Float, nullable=True)
    suhumin = db.Column(db.Float, nullable=True)
    curahhujan = db.Column(db.Float, nullable=True)
    sinarmatahari = db.Column(db.Float, nullable=True)
    cuaca = db.Column(db.String, nullable=True)
    tekananudara = db.Column(db.Float, nullable=True)
    kelembapan7 = db.Column(db.Integer, nullable=True)
    kelembapan13 = db.Column(db.Integer, nullable=True)
    kelembapan18 = db.Column(db.Integer, nullable=True)
    kelembapanrata = db.Column(db.Float, nullable=True)
    anginkecrata = db.Column(db.Float, nullable=True)
    anginarah = db.Column(db.Float, nullable=True)
    anginkecmaks = db.Column(db.Float, nullable=True)
    anginarahrata = db.Column(db.Integer, nullable=True)
    waktu = db.Column(db.DateTime, nullable=True)
    bulan_teks = db.Column(db.String, nullable=True)
    kelembapanmaks = db.Column(db.Integer, nullable=True)
    kelembapanmin = db.Column(db.Integer, nullable=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
