from flask import Flask
from flask_smorest import Api
from resources.items import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from db import db
import models
import os


def create_app(db_url=None):
    app = Flask(__name__)


    app.config["PROPAGATE_EXCEPTIONS"] = True # Propaga uma excecao para podermos ver
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3" # Padrão para documentação API 
    app.config["OPENAPI_URL_PREFIX"] = "/" # onde é a raiz da API(rota) 
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") # Usa a conexao de banco desejada, mas o default seria o sqlite
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app) # Inicia o contexto do banco de dados com o app criado

    api = Api(app)

    with app.app_context():
        db.create_all()    # Quando se inicia, ele cria o banco de acordo com os modelos criados na pasta models

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app