from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import StoreSchema
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


blp = Blueprint("stores", __name__, description="Operacoes nas lojas." )


@blp.route("/store/int:id_loja>")
class Store(MethodView):
    @blp.response(200, StoreSchema) # Decorator
    def get(self, id_loja):
        store = StoreModel.query.get_or_404(id_loja)
        return store
       

    def delete(self, id_loja):
        store = StoreModel.query.get_or_404(id_loja)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Loja Deletada"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True)) # Decorator
    def get(self):
        return StoreModel.query.all()
    

    @blp.arguments(StoreSchema) # Decorator
    @blp.response(200, StoreSchema) # Decorator
    def post(self, store_data):

        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Uma loja com esse nome ja existe.")
        except SQLAlchemyError:
            abort(500, message="Um erro ocorreu enquanto os dados estavam sendo inseridos.")

        return store