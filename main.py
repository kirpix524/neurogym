import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug import Response

from app.config import SQL_DATA, SECRET_KEY, TEMPLATES_DIRECTORY

from app.infrastructure.db.models import db, User

def create_app() -> Flask:
    db_file = os.path.abspath(SQL_DATA['db_path'])
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    templates_dir = os.path.join(os.path.dirname(__file__), TEMPLATES_DIRECTORY)

    app = Flask(__name__, template_folder=templates_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    db.init_app(app)

    @app.route('/register', methods=['GET'])
    def show_register_form() -> str:
        return render_template('register.html')

    @app.route('/register', methods=['POST'])
    def register_user() -> Response:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Все поля обязательны для заполнения.', 'error')
            return redirect(url_for('show_register_form'))

        if User.query.filter_by(email=email).first() is not None:
            flash('Пользователь с таким email уже существует.', 'error')
            return redirect(url_for('show_register_form'))

        new_user = User(email=email)
        new_user.password = password  # через сеттер свойство будет захешировано

        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('show_register_form'))

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
