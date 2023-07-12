import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import items
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("Items", __name__, description="Operacoes nos itens." )

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema) # Decorator
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item nao encontrado.")


    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message" : "Item deletado."}
        except KeyError:
            abort(404, message="Item nao encontrado.")


    @blp.arguments(ItemUpdateSchema) # Decorator
    @blp.response(200, ItemSchema) # Decorator
    def put(self, item_data, item_id):
       
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item nao encontrado.")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) # Decorator
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema) # Decorator
    @blp.response(201, ItemSchema) # Decorator
    def post(self, item_data):

        for item in items.values():
            if (item_data['nome'] == item['nome'] and item_data['id_loja'] == item['id_loja']):
                abort(400, message=f"Item ja existe.")

        
        item_id = uuid.uuid4().hex # Cria ID Universal
        new_item = {**item_data, "id": item_id}
        items[item_id] = new_item
        return new_item, 201