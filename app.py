from tda import auth, client
import os, json, datetime
from chalice import Chalice
from chalicelib import config2

app = Chalice(app_name='my_app')
token_path = os.path.join(os.path.dirname(__file__), 'chalicelib', 'token')

c = auth.client_from_token_file(token_path, config2.api_key)
#Define the routes of our AWS server once deployed
@app.route('/quote/{symbol}')
def quote(symbol):
#GET from API
    response = c.get_quote(symbol)
    return response.json()

@app.route('/hello')
def index():
  #GET from API
    return {'hello': 'world'}

@app.route('/option/order', methods=['POST'])
#IMPORTANT to post orders in TD API
def option_order():
    #receive our buy/sell message via JSON 
    webhook_message = app.current_request.json_body

    print(webhook_message)

    #secure our server and account with a password. Incase end point is discovered
    if 'passphrase' not in webhook_message:
        return {
            "code": "error",
            "message": "Unauthorized, no passphrase"
        }

    if webhook_message['passphrase'] != config2.passphrase:
        return {
            "code": "error",
            "message": "Invalid passphrase"
        }
    # taken from TD API order structures. Possible to update and make more intense
    # I should add a way to 
    order_spec = {
        "orderType": "MARKET",
        "session": "NORMAL",
        "duration": "DAY",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
                "instruction": webhook_message["instruction"], #string
              # Python parses the JSON as a dictionary. This is really useful for accessing our API post request
                "quantity": webhook_message["quantity"], # int
                "instrument": {
                    "symbol": webhook_message["symbol"], #string
                    "assetType": "OPTION"
                }
            }
        ]
    }



    # validate order in our API
    response = c.place_order(config2.account_id, order_spec)
    return {
        "code": "ok"
    }

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
