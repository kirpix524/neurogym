from flask import Blueprint

bp = Blueprint('trainings', __name__, url_prefix='/account/trainings', template_folder='templates')

from . import routes