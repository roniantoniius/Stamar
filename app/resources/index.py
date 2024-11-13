from flask import render_template, Blueprint, request, jsonify
from flask import Blueprint
from app.components.kpi import get_last_update
from app.components.etl import etl_process
from app.exts import db
import os

index_blueprint = Blueprint('index', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@index_blueprint.route('/')
def index():
    """Renders the index page"""
    session = db.session
    latest_update = get_last_update(session=session)
    return render_template('index.html', last_update=latest_update)

@index_blueprint.route('/login')
def login():
    return render_template('login.html')

@index_blueprint.route('/upload_data', methods=['POST'])
def upload_data():
    file = request.files.get('file')
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        try:
            result = etl_process(file_path)
            return jsonify({"message": result})
        finally:
            os.remove(file_path)
    return jsonify({"message": "File tidak ditemukan"}), 400