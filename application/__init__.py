from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


def init_app():
    # Inicia o app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Inicia o plugin do banco
    # db.init_app(app)

    with app.app_context():
        # Include our Routes
        from .usuario import routes as usuario

        # Register Blueprints
        app.register_blueprint(usuario.usuario_bp)

        return app
