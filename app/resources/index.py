from flask import render_template
from flask import Blueprint

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/')
def index():
    """Renders the index page"""
    return render_template('index.html')

@index_blueprint.route('/login')
def login():
    return render_template('login.html')