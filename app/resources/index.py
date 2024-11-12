from flask import render_template
from flask import Blueprint
from app.components.kpi import get_last_update
from app.exts import db

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/')
def index():
    """Renders the index page"""
    session = db.session
    latest_update = get_last_update(session=session)
    return render_template('index.html', last_update=latest_update)

@index_blueprint.route('/login')
def login():
    return render_template('login.html')