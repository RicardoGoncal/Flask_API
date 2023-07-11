from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "loja": "Minha Loja",
        "itens":[
            {
                "nome":"Cadeira",
                "preco": 25.90
            }
        ]
    }
]

@app.get("/store") # http://localhost:5000/store
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"loja": request_data["loja"], "itens":[]}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:loja>/item")
def create_item(loja):
    request_data = request.get_json()
    for store in stores:
        if store["loja"] == loja:
            new_item = {"nome": request_data["nome"], "preco": request_data["preco"]}
            store["itens"].append(new_item)
            return new_item, 201
    
    return {"mensagem": "Loja nao encontrada."}, 404


@app.get("/store/<string:loja>")
def get_store(loja):
    for store in stores:
        if store["loja"] == loja:
            return store, 201
    
    return {"mensagem": "Loja nao encontrada."}, 404


@app.get("/store/<string:loja>/item")
def get_item_in_store(loja):
    for store in stores:
        if store["loja"] == loja:
            return {"itens": store["itens"]}, 201
    
    return {"mensagem": "Loja nao encontrada."}, 404