from flask import Flask
from app.config import config
from app.extensions import login_manager
from app.database import close_db, init_users_db


def create_app(env: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[env])

    # Extensiones
    login_manager.init_app(app)

    # Teardown: cerrar conexiones DB al final de cada request
    app.teardown_appcontext(close_db)

    # Blueprints
    from app.auth import auth_bp
    from app.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Inicializar users.db si no existe
    init_users_db(app)

    # User loader para flask-login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

    return app
