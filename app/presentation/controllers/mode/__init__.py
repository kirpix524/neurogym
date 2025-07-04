from enum import Enum
from flask import Blueprint
class ModeOption(Enum):
    CUSTOM_INFO = "Произвольная информация"
    FOREIGN_LANGUAGES = "Иностранные языки"

bp = Blueprint('mode', __name__, url_prefix='/account/mode', template_folder='templates', static_folder='static')

from . import routes