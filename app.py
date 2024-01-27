from flask import Flask, request, jsonify
from coinbase.rest import RESTClient
from requests.exceptions import HTTPError
import os

app = Flask(__name__)

# Load API keys from environment variables or replace with your keys for testing
api_key = os.getenv('COINBASE_API_KEY', 'your_api_key')
api_secret = os.getenv('COINBASE_API_SECRET', 'your_api_secret')

# Initialize REST Client
client = RESTClient(api_key=api_key, api_secret=api_secret)

@app.route('/get_accounts', methods=['GET'])
def get_accounts():
    try:
        accounts = client.get_accounts()
        return jsonify(accounts), 200
    except HTTPError as e:
        return jsonify(error=str(e)), 400

@app.route('/create_order', methods=['POST'])
def create_order():
    try:
        data = request.json
        order = client.market_order_buy(client_order_id=data.get("client_order_id"), 
                                        product_id=data.get("product_id"), 
                                        quote_size=data.get("quote_size"))
        return jsonify(order), 200
    except HTTPError as e:
        return jsonify(error=str(e)), 400

@app.route('/get_product', methods=['GET'])
def get_product():
    try:
        product_id = request.args.get('product_id')
        product = client.get_product(product_id=product_id)
        return jsonify(product), 200
    except HTTPError as e:
        return jsonify(error=str(e)), 400

# Additional routes for other functionalities...

@app.route('/get_time', methods=['GET'])
def get_time():
    try:
        server_time = client.get_unix_time()
        return jsonify(server_time), 200
    except HTTPError as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)

