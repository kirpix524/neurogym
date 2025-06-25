from enum import Enum
from flask import Blueprint
class ModeOption(Enum):
    CUSTOM_INFO = "Произвольная информация"
    FOREIGN_LANGUAGES = "Иностранные языки"

bp = Blueprint('mode', __name__, url_prefix='/mode', template_folder='templates')

from . import mode_routes