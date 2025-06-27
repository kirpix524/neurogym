import os
from flask import Flask, session, g


from app.config import SQL_DATA, SECRET_KEY, TEMPLATES_DIRECTORY, STATIC_DIRECTORY

from app.infrastructure.db import db
from app.infrastructure.db.models.user import User
from app.presentation.controllers.mode import bp as mode_bp, ModeOption
from app.presentation.controllers.account_settings import bp as account_settings_bp
from app.presentation.controllers.register import bp as register_bp
from app.presentation.controllers.login import bp as login_bp
from app.presentation.controllers.user_trainings import bp as user_trainings_bp
from app.presentation.controllers.user_data import bp as user_data_bp
from app.presentation.controllers.core import bp as core_bp


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

    flask_app.register_blueprint(core_bp)
    flask_app.register_blueprint(mode_bp)
    flask_app.register_blueprint(account_settings_bp)
    flask_app.register_blueprint(register_bp)
    flask_app.register_blueprint(login_bp)
    flask_app.register_blueprint(user_trainings_bp)
    flask_app.register_blueprint(user_data_bp)

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

    return flask_app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
