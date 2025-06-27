from flask import render_template, request, redirect, url_for, flash, g, Response
from app.infrastructure.db.models.user import User
from app.infrastructure.db import db
from . import bp

@bp.route('/', methods=['GET', 'POST'])
def account_settings() -> Response | str:
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    if request.method == 'POST':
        username: str           = request.form.get('username', '').strip()
        email: str              = request.form.get('email', '').strip().lower()
        old_password: str       = request.form.get('old_password', '')
        new_password: str       = request.form.get('password', '')
        confirm_password: str   = request.form.get('password_confirm', '')

        changed: bool = False

        if email and email != g.current_user.email:
            existing: User | None = User.query.filter_by(email=email).first()
            if existing:
                flash('Пользователь с таким email уже существует.', 'error')
                return redirect(url_for('account_settings.account_settings'))
            g.current_user.email = email
            changed = True

        if username and username != g.current_user.username:
            g.current_user.username = username
            changed = True

        if new_password:
            if not g.current_user.check_password(old_password):
                flash('Старый пароль указан неверно.', 'error')
                return redirect(url_for('account_settings.account_settings'))

            if new_password != confirm_password:
                flash('Новые пароли не совпадают.', 'error')
                return redirect(url_for('account_settings.account_settings'))

            g.current_user.password = new_password
            changed = True

        if changed:
            db.session.commit()
            flash('Настройки сохранены.', 'success')
        else:
            flash('Вы ничего не изменили.', 'error')

        return redirect(url_for('account_settings.account_settings'))

    return render_template('account_settings.html')
