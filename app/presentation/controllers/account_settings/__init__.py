from flask import Blueprint
bp = Blueprint('account_settings', __name__, url_prefix='/account', template_folder='templates')
from . import account_settings_routes