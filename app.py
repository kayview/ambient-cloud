from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, random
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Kayview API LIVE"})

@app.route("/scanner/analyse", methods=["POST"])
def scanner():
    data = request.json or {}
    pair = data.get("pair", "XAUUSD")
    tf = data.get("timeframe", "M15")
    base = 46.08 + random.uniform(-0.2, 0.2)
    bid = round(base - 0.0023, 5)
    ask = round(base + 0.0023, 5)
    direction = random.choice(["BUY", "SELL"])
    return jsonify({
        "pair": pair, "timeframe": tf, "bid": bid, "ask": ask,
        "spread": round(ask-bid, 5),
        "setup": "Liquidity Sweep + MSS + Order Block Entry",
        "direction": direction, "htfBias": "bullish", "zone": "premium",
        "details": [
            f"BSL liquidity sweep @ {bid-0.08:.3f}",
            f"BOS {direction.lower()} @ {bid-0.15:.3f}",
            f"Supply OB {bid-0.4:.2f}-{bid-0.35:.2f}",
            f"premium zone (EQ {bid-3:.4f})"
        ],
        "entry": f"{bid-0.05:.3f}",
        "sl": f"{bid+0.03:.4f}",
        "tp1": f"{bid-0.10:.4f}",
        "tp2": f"{bid-0.13:.4f}"
    })

@app.route("/mt5/accounts", methods=["POST"])
def add_mt5():
    data = request.json or {}
    return jsonify({"success": True, "account": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)