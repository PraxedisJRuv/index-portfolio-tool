""""
This is by far the worst test, it takes notice it was the only one developed with the most AI since it fails in
Many regards and it's just bad, but it had some interesting ideas, that could work for future proyects, That's
why I'm saving it
"""


# config
TICKERS = {
    "AAPL": 0.30,
    "MSFT": 0.30,
    "NVDA": 0.20,
    "AMZN": 0.20
}

BASE_VALUE = 100

#Engine
import redis
from config import TICKERS, BASE_VALUE

r = redis.Redis(host="localhost", port=6379)

base_prices = {}
current_prices = {}

def initialize_base_prices(prices):
    global base_prices
    base_prices = prices

def update_price(symbol, price):
    current_prices[symbol] = price

def compute_index():
    index = 0
    for symbol, weight in TICKERS.items():
        if symbol not in base_prices:
            return None
        price_rel = current_prices[symbol] / base_prices[symbol]
        index += weight * price_rel

    index *= BASE_VALUE

    r.set("index_value", index)

    return index

#Real time stream
import websocket
import json
from index_calculator import update_price, compute_index

API_KEY = "YOUR_KEY"

def on_message(ws, message):
    data = json.loads(message)
    for trade in data:
        symbol = trade.get("sym")
        price = trade.get("p")
        if symbol:
            update_price(symbol, price)
            index = compute_index()
            if index:
                print("Index:", index)


def on_open(ws):

    auth = {"action": "auth", "params": API_KEY}
    ws.send(json.dumps(auth))
    subs = "T.AAPL,T.MSFT,T.NVDA,T.AMZN"
    ws.send(json.dumps({
        "action": "subscribe",
        "params": subs
    }))


socket = websocket.WebSocketApp(
    "wss://socket.polygon.io/stocks",
    on_open=on_open,
    on_message=on_message
)

socket.run_forever()