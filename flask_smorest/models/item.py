from db import db

# Modelo para criar o banco de dados de Itens
class ItemModel(db.Model):
    __tablename__ = "items"

    id_item = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    preco = db.Column(db.Float(precision=2), unique=True, nullable=False)
    id_loja = db.Column(db.Integer, db.ForeignKey("stores.id_loja"), unique=True, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")