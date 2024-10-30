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

    def __init__(self, nosta, namasta, tahun, bulan, tgl, suhu7, suhu13, suhu18,
                 suhurata, suhumaks, suhumin, curahhujan, sinarmatahari,
                 cuaca, tekananudara, kelembapan7, kelembapan13,
                 kelembapan18, kelembapanrata, anginkecrata, anginarah,
                 anginkecmaks, anginarahrata, waktu, bulan_teks,
                 kelembapanmaks, kelembapanmin):
        self.nosta = nosta
        self.namasta = namasta
        self.tahun = tahun
        self.bulan = bulan
        self.tgl = tgl
        self.suhu7 = suhu7
        self.suhu13 = suhu13
        self.suhu18 = suhu18
        self.suhurata = suhurata
        self.suhumaks = suhumaks
        self.suhumin = suhumin
        self.curahhujan = curahhujan
        self.sinarmatahari = sinarmatahari
        self.cuaca = cuaca
        self.tekananudara = tekananudara
        self.kelembapan7 = kelembapan7
        self.kelembapan13 = kelembapan13
        self.kelembapan18 = kelembapan18
        self.kelembapanrata = kelembapanrata
        self.anginkecrata = anginkecrata
        self.anginarah = anginarah
        self.anginkecmaks = anginkecmaks
        self.anginarahrata = anginarahrata
        self.waktu = waktu
        self.bulan_teks = bulan_teks
        self.kelembapanmaks = kelembapanmaks
        self.kelembapanmin = kelembapanmin

    def to_dict(self):
        return {
            'id': self.id,
            'nosta': self.nosta,
            'namasta': self.namasta,
            'tahun': self.tahun,
            'bulan': self.bulan,
            'tgl': self.tgl,
            'suhu7': self.suhu7,
            'suhu13': self.suhu13,
            'suhu18': self.suhu18,
            'suhurata': self.suhurata,
            'suhumaks': self.suhumaks,
            'suhumin': self.suhumin,
            'curahhujan': self.curahhujan,
            'cuaca': self.cuaca,
            'tekananudara': self.tekananudara,
            'kelembapan7': self.kelembapan7,
            'kelembapan13': self.kelembapan13,
            'kelembapan18': self.kelembapan18,
            'kelembapanrata': self.kelembapanrata,
            'anginkecrata': self.anginkecrata,
            'anginarah': self.anginarah,
            'anginkecmaks': self.anginkecmaks,
            'anginarahrata': self.anginarahrata,
            'waktu': self.waktu,
            'bulan_teks': self.bulan_teks,
            'kelembapanmaks': self.kelembapanmaks,
            'kelembapanmin': self.kelembapanmin
        }