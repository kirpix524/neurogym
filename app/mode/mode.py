from enum import Enum
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug import Response


class ModeOption(Enum):
    CUSTOM_INFO = "Произвольная информация"
    FOREIGN_LANGUAGES = "Иностранные языки"

bp = Blueprint('mode', __name__, url_prefix='/mode', template_folder='templates')

@bp.route('/select', methods=['GET', 'POST'])
def select_mode() -> Response | str:
    """
    Отображает форму выбора режима и обрабатывает отправку.
    """
    if request.method == 'POST':
        selected_mode: str = request.form.get('mode', '')
        session['mode'] = selected_mode  # сохраняем выбранный режим в сессии
        return redirect(url_for('mode.select_mode'))
    return render_template('select_mode.html', modes=ModeOption, current_mode=session.get('mode'))
