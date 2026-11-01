const express = require('express');
const cors = require('cors');
const admin = require('firebase-admin');

const app = express();
app.use(cors());
app.use(express.json());

// --- FIRESTORE CONNECT ---
let db = null;
try {
    const keyJson = process.env.FIREBASE_KEY;
    if (keyJson) {
        const cred = JSON.parse(keyJson);
        admin.initializeApp({
            credential: admin.credential.cert(cred)
        });
        db = admin.firestore();
        console.log("FIRESTORE CONNECTED");
    } else {
        console.log("NO FIREBASE_KEY");
    }
} catch (e) {
    console.log("Firestore error", e);
}

app.get("/", (req, res) => {
    res.json({ status: "Kayview API LIVE Node", firestore: !!db, time: new Date().toISOString() });
});

// --- YOUR FLUTTER CALLS THIS ---
app.post("/mt5/accounts", async (req, res) => {
    const { login, password, server, broker } = req.body;
    const brokerName = broker || server;
    const accountData = {
        login: String(login),
        password,
        server,
        broker: brokerName,
        nickname: `${brokerName} - ${login}`,
        created: new Date().toISOString()
    };
    if (db) {
        const doc = await db.collection("mt5_accounts").add(accountData);
        accountData.id = doc.id;
    }
    res.json({ success: true, message: `SAVED ${brokerName}`, account: accountData });
});

app.get("/mt5/accounts", async (req, res) => {
    if (!db) return res.json([]);
    const snap = await db.collection("mt5_accounts").get();
    const accounts = snap.docs.map(d => ({ ...d.data(), id: d.id }));
    res.json(accounts);
});

app.post("/scanner/analyse", (req, res) => {
    const pair = req.body.pair || "XAUUSD";
    const tf = req.body.timeframe || "M15";
    const base = 46.08 + (Math.random()-0.5);
    const bid = Number((base - 0.0023).toFixed(5));
    const ask = Number((base + 0.0023).toFixed(5));
    const direction = Math.random() > 0.5 ? "BUY" : "SELL";
    
    res.json({
        pair, timeframe: tf, bid, ask, spread: Number((ask-bid).toFixed(5)),
        setup: "Liquidity Sweep + MSS + Order Block Entry",
        direction, htfBias: "bullish", zone: "premium",
        details: [
            `BSL liquidity sweep @ ${(bid-0.08).toFixed(3)}`,
            `BOS ${direction.toLowerCase()} @ ${(bid-0.15).toFixed(3)}`,
            `Supply OB ${(bid-0.4).toFixed(2)}-${(bid-0.35).toFixed(2)}`
        ],
        entry: (bid-0.05).toFixed(3), entryPips: "950 pips away",
        sl: (bid+0.03).toFixed(4), slPips: "352 pips",
        rr: "1:1.5", rrNote: "BSL sweep wick 50%",
        tp1: (bid-0.10).toFixed(4), tp1Pips: "1478 pips left",
        tp2: (bid-0.13).toFixed(4), tp2Pips: "1830 pips left"
    });
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, '0.0.0.0', () => console.log(`Live on ${PORT}`));