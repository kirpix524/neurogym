from flask import render_template, request, redirect, url_for, session
from werkzeug import Response
from . import bp, ModeOption

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
