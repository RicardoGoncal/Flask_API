from marshmallow import Schema, fields

"""
Area destinada a criar um esquema de definicao dos parametros que 
serao recebidos via body de um POST ou URL de um GET
"""

"""
Plano de esquema para itens sem ter relacao com store.
Aqui somente campos que tem relação com os itens
"""
class PlainItemSchema(Schema):
    item_id = fields.Str(dump_only=True)
    nome = fields.Str(required=True)
    price = fields.Float(required=True)
  

"""
Plano de esquema para lojas sem ter relacao com items.
Aqui somente campos que tem relação com as lojas
"""
class PlainStoreSchema(Schema):
    id_loja = fields.Str(dump_only=True)
    nome = fields.Str(required=True)


"""
Plano de esquema para update de itens 
"""
class ItemUpdateSchema(Schema):
    nome = fields.Str()
    preco = fields.Float()
    id_loja = fields.Int()

"""
Esquema de itens com os campos definidos no plano + id_loja
Temos aqui uma relacao com o plano de lojas, qual possui campos de loja
"""
class ItemSchema(PlainItemSchema):
    id_loja = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

"""
Esquema de lojas com os campos definidos no plano + items
Temos aqui uma relacao com o plano de itens, qual vai trazer uma lista de itens
"""
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)