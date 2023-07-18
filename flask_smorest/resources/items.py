from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from flask_wt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from db import db


blp = Blueprint("Items", __name__, description="Operacoes nos itens." )

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema) # Decorator
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deletado"}


    @blp.arguments(ItemUpdateSchema) # Decorator
    @blp.response(200, ItemSchema) # Decorator
    def put(self, item_data, item_id):
       
        item = ItemModel.query.get(item_id)
        if item:
            item.preco = item_data["preco"]
            item.nome = item_data["nome"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True)) # Decorator
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required()
    @blp.arguments(ItemSchema) # Decorator
    @blp.response(201, ItemSchema) # Decorator
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="Um erro ocorreu enquanto os dados estavam sendo inseridos.")

        return item