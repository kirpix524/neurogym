from flask import render_template, request, redirect, url_for, session, g, flash
from werkzeug import Response
from . import bp, ModeOption

@bp.route('/', methods=['GET', 'POST'])
def select_mode() -> Response | str:
    """
    Отображает форму выбора режима и обрабатывает отправку.
    """
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    if 'mode' not in session:
        session['mode'] = ModeOption.CUSTOM_INFO.value
    if request.method == 'POST':
        selected_mode: str = request.form.get('mode', '')
        session['mode'] = selected_mode  # сохраняем выбранный режим в сессии
        return redirect(url_for('mode.select_mode'))
    return render_template('select_mode.html', modes=ModeOption, current_mode=session.get('mode'))
