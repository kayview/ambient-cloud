from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Kayview API LIVE", "connected": True})

@app.route("/scanner/analyse", methods=["POST", "GET", "OPTIONS"])
def analyse():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200
    
    try:
        body = request.get_json(force=True, silent=True) or {}
        pair = body.get("pair", "XAUUSD")
    except:
        pair = "XAUUSD"
    
    bid = round(46.08 + random.uniform(-0.5, 0.5), 5)
    ask = round(bid + 0.0046, 5)

    return jsonify({
        "pair": pair,
        "bid": bid,
        "ask": ask,
        "spread": round(ask-bid,5),
        "setup": "Liquidity Sweep + MSS + OB",
        "direction": random.choice(["BUY", "SELL"]),
        "htfBias": "bullish",
        "entry": f"{bid}",
        "sl": f"{bid+0.3:.2f}",
        "tp1": f"{bid-0.5:.2f}",
        "tp2": f"{bid-0.8:.2f}"
    })

@app.route("/mt5/accounts", methods=["GET","POST","OPTIONS"])
def accounts():
    return jsonify({"success": True, "accounts": []})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
