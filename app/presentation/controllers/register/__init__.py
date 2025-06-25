from flask import Blueprint

bp = Blueprint('register', __name__, url_prefix='/register', template_folder='templates')

from . import routes