from flask import Blueprint

bp = Blueprint('word_pairs', __name__, url_prefix='/account/data/pairs', template_folder='templates', static_folder='static')

from . import routes