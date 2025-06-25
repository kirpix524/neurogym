from flask import Blueprint

bp = Blueprint('login', __name__, url_prefix='/login', template_folder='templates')

from . import routes