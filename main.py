from fastapi import FastAPI
from datetime import datetime

app = FastAPI()
signals_db = []

@app.get("/")
def home():
    return {"status": "Prime Host Cloud is LIVE", "ea": "LS ICT V7", "signals": len(signals_db)}

@app.post("/api/signal")
def receive_signal(data: dict):
    data["received_at"] = datetime.utcnow().isoformat()
    signals_db.append(data)
    # Keep last 100
    if len(signals_db) > 100:
        signals_db.pop(0)
    print(f"NEW SIGNAL: {data}")
    return {"received": True, "total_signals": len(signals_db)}

@app.get("/api/signals")
def get_signals():
    return {"count": len(signals_db), "signals": signals_db[-20:]}

@app.get("/health")
def health():
    return {"ok": True, "cloud": "ambient-cloud-2"}
