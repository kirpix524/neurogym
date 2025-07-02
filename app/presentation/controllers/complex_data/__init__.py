from flask import Blueprint

bp = Blueprint('complex_data', __name__, url_prefix='/account/data/complex', template_folder='templates')

from . import routes