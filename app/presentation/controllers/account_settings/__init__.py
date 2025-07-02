from flask import Blueprint
bp = Blueprint('account_settings', __name__, url_prefix='/account/settings', template_folder='templates', static_folder='static')
from . import routes