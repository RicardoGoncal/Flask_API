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
    item_id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    preco = fields.Float(required=True)
  

"""
Plano de esquema para lojas sem ter relacao com items.
Aqui somente campos que tem relação com as lojas
"""
class PlainStoreSchema(Schema):
    id_loja = fields.Int(dump_only=True)
    nome = fields.Str(required=True)


"""
Plano de esquema para tags sem ter relacao com lojas
Aqui somente campos que tem relação com as tags
"""
class PlainTagSchema(Schema):
    tag_id = fields.Int(dump_only=True)
    nome = fields.Str()


"""
Plano de esquema para update de itens 
"""
class ItemUpdateSchema(Schema):
    nome = fields.Str()
    preco = fields.Float()


"""
Esquema de itens com os campos definidos no plano + id_loja
Temos aqui uma relacao com o plano de lojas, qual possui campos de loja
"""
class ItemSchema(PlainItemSchema):
    id_loja = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


"""
Esquema de lojas com os campos definidos no plano + items
Temos aqui uma relacao com o plano de itens, qual vai trazer uma lista de itens
"""
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


"""
Esquema de tags com os campos definidos no plano + id_loja
Temos aqui uma relacao com o plano de lojas, qual possui campos de loja
"""
class TagSchema(PlainTagSchema):
    id_loja = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


"""
Esquema para trabalhar com relação N para N no banco de dados
O que seria uma TAG associada a um item da loja 
"""
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


"""
Esquema de usuario e senha para gerir o JWT
JWT: token para uso da API de acordo com a autenticação do usuario
"""
class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)