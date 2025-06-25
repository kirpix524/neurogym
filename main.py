import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, Response
from werkzeug import Response

from app.config import SQL_DATA, SECRET_KEY, TEMPLATES_DIRECTORY, STATIC_DIRECTORY

from app.infrastructure.db.models import db, User
from app.presentation.controllers.mode import bp as mode_bp, ModeOption
from app.presentation.controllers.account_settings import bp as account_settings_bp
from app.presentation.controllers.register import bp as register_bp


def create_app() -> Flask:
    db_file = os.path.abspath(SQL_DATA['db_path'])
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    templates_dir = os.path.join(os.path.dirname(__file__), TEMPLATES_DIRECTORY)
    static_dir = os.path.join(os.path.dirname(__file__), STATIC_DIRECTORY)

    flask_app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SECRET_KEY'] = SECRET_KEY
    db.init_app(flask_app)

    flask_app.register_blueprint(mode_bp)
    flask_app.register_blueprint(account_settings_bp)
    flask_app.register_blueprint(register_bp)

    @flask_app.route('/', methods=['GET'])
    def home() -> str:
        return render_template('index.html')

    @flask_app.route('/signin', methods=['GET'])
    def show_signin_form() -> str:
        return render_template('signin.html')

    @flask_app.route('/signin', methods=['POST'])
    def signin_user() -> Response | str:
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Все поля обязательны для заполнения.', 'error')
            return redirect(url_for('show_signin_form'))

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Неверный email или пароль.', 'error')
            return redirect(url_for('show_signin_form'))

        session['user_id'] = user.id
        flash('Вы успешно вошли!', 'success')
        return redirect(url_for('account_settings.account_settings'))

    @flask_app.route('/logout')                     # ← новый маршрут выхода
    def logout() -> Response:
        session.pop('user_id', None)
        flash('Вы вышли из системы.', 'success')
        return redirect(url_for('home'))

    @flask_app.before_request  # ← загружаем пользователя в g
    def load_current_user() -> None:
        g.current_user = None
        user_id = session.get('user_id')
        if user_id is not None:
            g.current_user = User.query.get(user_id)

    @flask_app.context_processor  # ← делаем current_user доступным в шаблонах
    def inject_user():
        return dict(current_user=g.current_user)

    @flask_app.context_processor
    def inject_current_mode():
        default = ModeOption.CUSTOM_INFO.value
        return {'current_mode': session.get('mode', default)}

    @flask_app.route('/account/data', methods=['GET'])
    def user_data():
        return render_template('user_data.html')

    @flask_app.route('/account/training', methods=['GET'])
    def user_trainings():
        return render_template('user_trainings.html')



    return flask_app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
