from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"id": 1, "name": request.args.get('itemName'), "rank": 3, "price": 10})

@app.route('/fetch', methods=['POST'])
def fetch():
    itemName = request.json['itemName']
    rank = request.json['rank']
    if rank == "":
        response = requests.get(f"https://api.warframe.market/v1/items/{itemName}/orders?include=item").json()
        itemVal = response['include']['item']['items_in_set'][0]
        formated = [element for element in response['payload']['orders'] if element['order_type'] == "sell" and element['user']['status'] == "ingame"]
        formated.sort(key=lambda x: x['platinum'])
        final = formated[0]
        final["item"] = itemVal
        return jsonify(final)
    else:
        rank = int(rank)
        if rank > 5:
            return jsonify({"mod_rank": "error"})
        else:
            response = requests.get(f"https://api.warframe.market/v1/items/{itemName}/orders?include=item").json()
            itemVal = response['include']['item']['items_in_set'][0]
            if response['payload']['orders'][0]['mod_rank'] == None:
                return jsonify({"mod_rank": "error"})
            else:
                formated = [element for element in response['payload']['orders'] if element['mod_rank'] == rank and element['order_type'] == "sell" and element['user']['status'] == "ingame"]
                formated.sort(key=lambda x: x['platinum'])
                final = formated[0]
                final["item"] = itemVal
                return jsonify(final)

@app.route('/onchangehint', methods=['POST'])
def onchangehint():
    itemName = request.json['itemName']
    if itemName != "":
        response = requests.get("https://api.warframe.market/v1/items").json()
        formated = [element for element in response['payload']['items'] if itemName in element['item_name'] or itemName in element['url_name']]
        return jsonify(formated)
    else:
        return jsonify([])

@app.route('/onchangehintv2', methods=['POST'])
def onchangehintv2():
    response = requests.get("https://api.warframe.market/v1/items").json()
    return jsonify(response['payload']['items'])

if __name__ == '__main__':
    app.run()
