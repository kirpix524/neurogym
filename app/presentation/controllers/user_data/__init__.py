from flask import Blueprint

bp = Blueprint('data', __name__, url_prefix='/account/data', template_folder='templates', static_folder='static')

from . import routes