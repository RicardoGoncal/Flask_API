import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


# Uso de um DB.py para armazenar. Ver arquivo criado na pasta flask_smorest
# stores = {}
# items = {}

@app.get("/store") # http://localhost:5000/store
def get_all_stores():
    return {"stores": list(stores.values())}


@app.get("/item") # http://localhost:5000/item
def get_all_items():
    return {"items": list(items.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json() # Coleta body da requisição POST

    if ("nome" not in store_data):
        abort(400, message="Bad request. Ensure 'name' are included in the JSON payload.",)

    for store in store.values():
        if (store_data['nome'] == store['nome']):
            abort(400, message=f"Loja ja existe.")

    store_id = uuid.uuid4().hex # Cria ID Universal
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.post("/item")
def create_item():
    item_data = request.get_json()

    if ("price" not in item_data or "id_loja" not in item_data or "nome" not in item_data):
        abort(400, message="Bad request. Ensure 'price', 'stored_id', and 'name' are included in the JSON payload.",)

    for item in items.values():
        if (item_data['nome'] == item['nome'] and item_data['id_loja'] == item['id_loja']):
            abort(400, message=f"Item ja existe.")

    if item_data['id_loja'] not in stores:
        abort(404, message="Loja nao encontrada.")
    

    item_id = uuid.uuid4().hex # Cria ID Universal
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item
    return new_item, 201
    

@app.get("/store/<string:id_loja>")
def get_store(id_loja):
    try:
        return stores[id_loja]
    except KeyError:
        abort(404, message="Loja nao encontrada.")
    
 
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item nao encontrado.")