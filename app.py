from quart import Quart, request, jsonify, send_file, Response
from coinbase.rest import RESTClient
from requests.exceptions import HTTPError
import quart_cors
from quart_cors import cors
import os

app = cors(Quart(__name__), allow_origin="*")

# Load API keys from environment variables or replace with your keys for testing
api_key = os.getenv('COINBASE_API_KEY', 'your_api_key')
api_secret = os.getenv('COINBASE_API_SECRET', 'your_api_secret')

coinbase_client_id = os.getenv('COINBASE_CLIENT_ID', 'your_client_id')
coinbase_client_secret = os.getenv('COINBASE_CLIENT_SECRET', 'your_client_secret')
coinbase_code = os.getenv('COINBASE_CODE', 'your_code')
coinbase_token = os.getenv('COINBASE_TOKEN', 'your_token')

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
async def create_order():
    try:
        data = await request.get_json()
        order = client.market_order_buy(client_order_id=data.get("client_order_id"), 
                                        product_id=data.get("product_id"), 
                                        quote_size=data.get("quote_size"))
        return jsonify(order), 200
    except HTTPError as e:
        return jsonify(error=str(e)), 400

@app.route('/get_products', methods=['GET'])
def get_products():
    try:
        accounts = client.get_products()
        return jsonify(accounts), 200
    except HTTPError as e:
        return jsonify(error=str(e)), 400

@app.route('/get_product/<string:product_id>', methods=['GET'])
async def get_product(product_id):
    try:
        product = client.get_product(product_id=product_id)
        return jsonify(product), 200
    except HTTPError as e:
        return jsonify(error=str(e)), 400


@app.route('/get_time', methods=['GET'])
async def get_time():
    try:
        server_time = client.get_unix_time()
        return jsonify(server_time), 200
    except HTTPError as e:
        return jsonify(error=str(e)), 400

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return Response(text, mimetype="text/yaml")

@app.get("/oauth")
async def oauth():
    query_string = request.query_string.decode('utf-8')
    parts = query_string.split('&')
    kvps = {}
    for part in parts:
        k, v = part.split('=')
        v = v.replace("%2F", "/").replace("%3A", ":")
        kvps[k] = v
    print("OAuth key value pairs from the ChatGPT Request: ", kvps)
    url = kvps["redirect_uri"] + f"?code={OPENAI_CODE}"
    print("URL: ", url)
    return quart.Response(
        f'<a href="{url}">Click to authorize</a>'
    )

@app.post("/auth/oauth_exchange")
async def oauth_exchange():
    request = await quart.request.get_json(force=True)
    print(f"oauth_exchange {request=}")

    if request["client_id"] != coinbase_client_id:
        raise RuntimeError("bad client ID")
    if request["client_secret"] != coinbase_client_secret:
        raise RuntimeError("bad client secret")
    if request["code"] != coinbase_code:
        raise RuntimeError("bad code")

    return {
        "access_token": coinbase_token,
        "token_type": "bearer"
    }


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5003, use_reloader=True)

