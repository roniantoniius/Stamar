from flask import render_template
from flask import Blueprint

# Membuat blueprint untuk halaman index
index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/')
def index():
    """Renders the index page"""
    return render_template('index.html')