from flask import render_template, request, redirect, url_for, flash, session, g, Response
from app.infrastructure.db.models.user import User

from . import bp

@bp.route('/', methods=['GET'])
def show_login_form() -> str:
    return render_template('login.html')

@bp.route('/', methods=['POST'])
def login() -> Response | str:
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Все поля обязательны для заполнения.', 'error')
        return redirect(url_for('show_login_form'))

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        flash('Неверный email или пароль.', 'error')
        return redirect(url_for('show_login_form'))

    session['user_id'] = user.id
    flash('Вы успешно вошли!', 'success')
    return redirect(url_for('account_settings.account_settings'))