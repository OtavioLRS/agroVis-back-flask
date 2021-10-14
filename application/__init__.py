from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

db = SQLAlchemy()


def init_app():
    # Inicia o app
    app = Flask(__name__, instance_relative_config=False)
    cors = CORS(app)
    app.config.from_object('config.Config')
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['AC'] = 'Content-Type'

    # Inicia o plugin do banco
    db.init_app(app)

    with app.app_context():
        # Importando as rotas
        from . import routes as home_bp
        from .usuario import routes as usuario
        from .cidade import routes as cidade
        from .sh4 import routes as sh4
        from .anotacao import routes as anotacao
        from .sh4_ncm import routes as sh4_ncm
        from .exportacao import routes as exportacao

        # Registrando blueprints
        app.register_blueprint(home_bp.home_bp)
        app.register_blueprint(usuario.usuario_bp)
        app.register_blueprint(cidade.cidade_bp)
        app.register_blueprint(sh4.sh4_bp)
        app.register_blueprint(anotacao.anotacao_bp)
        app.register_blueprint(sh4_ncm.sh4_ncm_bp)
        app.register_blueprint(exportacao.exportacao_bp)

        # Criando modelos do DB
        db.create_all()

        return app
