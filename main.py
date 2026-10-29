from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Prime Host Cloud is LIVE"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/signal")
def signal(data: dict):
    return {"received": True, "data": data}
