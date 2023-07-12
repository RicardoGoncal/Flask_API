from flask import Flask
from flask_smorest import Api
from resources.items import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)


app.config["PROPAGATE_EXCEPTIONS"] = True # Propaga uma excecao para podermos ver
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3" # Padrão para documentação API 
app.config["OPENAPI_URL_PREFIX"] = "/" # onde é a raiz da API(rota) 
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)