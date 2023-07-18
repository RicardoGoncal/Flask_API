from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.items import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from db import db
from blocklist import BLOCKLIST
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

    app.config["JWT_SECRET_KEY"] = "ricardo"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description": "O token foi revogado", "error": "Token revogado"}
            )
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {
                    "description": "Token nao esta fresh",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )


    with app.app_context():
        db.create_all()    # Quando se inicia, ele cria o banco de acordo com os modelos criados na pasta models

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app