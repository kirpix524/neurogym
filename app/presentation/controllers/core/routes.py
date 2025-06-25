from flask import render_template, session, flash, redirect, url_for, Response
from . import bp



@bp.route('/', methods=['GET'])
def home() -> str:
    return render_template('index.html')

@bp.route('/logout')                     # ← новый маршрут выхода
def logout() -> Response:
    session.pop('user_id', None)
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('core.home'))