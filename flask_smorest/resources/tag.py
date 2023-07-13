from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import TagSchema, TagAndItemSchema
from db import db
from models import TagModel, StoreModel, ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


blp = Blueprint("tags", __name__, description="Operacoes nas tags." )

@blp.route("/store/<string:id_loja>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, id_loja):
        store = StoreModel.query.get_or_404(id_loja)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, id_loja):
        if TagModel.query.filter(TagModel.id_loja == id_loja, TagModel.nome == tag_data["nome"]).first():
            abort(400, message="Uma tag com o mesmo nome ja existe nesta loja.")

        tag = TagModel(**tag_data, id_loja=id_loja)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Um erro ocorreu enquanto uma tag era inserida")
        
        return tag
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Um erro ocorreu enquanto uma tag era inserida")
        
        return {"message": "Item removido da tag", "item": item, "tag": tag}


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(
        202,
        description="Deleta tag se nao tem um item linkada a ela.",
        example={"message": "Tag deletada."}
    )
    @blp.alt_response(404, description="Tag nao encontrada")
    @blp.alt_response(
        400,
        description="Retorna se uma tag esta associada a 1 ou mais items. Neste caso, a tag nao é deletada."
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Ta deletada."}
        
        abort(
            400,
            message = "A tag nao pode ser deletada. Garanta que a tag nao esteja associada a nenhum item."
        )