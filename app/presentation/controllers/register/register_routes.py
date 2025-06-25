from . import bp
from flask import render_template, request, redirect, url_for, flash, session, g, Response
from app.infrastructure.db.models import db
from app.infrastructure.db.models import User

@bp.route('/register', methods=['GET'])
def show_register_form() -> str:
    return render_template('register.html')

@bp.route('/register', methods=['POST'])
def register_user() -> Response:
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Все поля обязательны для заполнения.', 'error')
        return redirect(url_for('register.show_register_form'))

    if User.query.filter_by(email=email).first() is not None:
        flash('Пользователь с таким email уже существует.', 'error')
        return redirect(url_for('register.show_register_form'))

    new_user = User(email=email)
    new_user.password = password  # через сеттер свойство будет захешировано

    db.session.add(new_user)
    db.session.commit()

    flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
    return redirect(url_for('show_signin_form'))