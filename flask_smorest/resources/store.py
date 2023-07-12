import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import stores
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operacoes nas lojas." )


@blp.route("/store/<string:id_loja>")
class Store(MethodView):
    @blp.response(200, StoreSchema) # Decorator
    def get(self, id_loja):
        try:
            return stores[id_loja]
        except KeyError:
            abort(404, message="Loja nao encontrada.")


    def delete(self, id_loja):
        try:
            del stores[id_loja]
            return {"message" : "Loja deletada."}
        except KeyError:
            abort(404, message="Loja nao encontrada.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True)) # Decorator
    def get(self):
        return {"stores": list(stores.values())}
    

    @blp.arguments(StoreSchema) # Decorator
    @blp.response(200, StoreSchema) # Decorator
    def post(self, store_data):

        for store in store.values():
            if (store_data['nome'] == store['nome']):
                abort(400, message=f"Loja ja existe.")

        store_id = uuid.uuid4().hex # Cria ID Universal
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store 