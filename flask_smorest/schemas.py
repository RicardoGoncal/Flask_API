from marshmallow import Schema, fields


class ItemSchema(Schema):
    item_id = fields.Str(dump_only=True)
    nome = fields.Str(required=True)
    price = fields.Float(required=True)
    id_loja = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    nome = fields.Str()
    preco = fields.Float()


class StoreSchema(Schema):
    id_loja = fields.Str(dump_only=True)
    nome = fields.Str(required=True)