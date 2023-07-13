from db import db

# Modelo para criar o banco de dados de Store
class StoreModel(db.Model):
    __tablename__ = "stores"

    id_loja = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")