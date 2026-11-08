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

// --- NEW: HEALTH for Prime Host + EA ---
app.get("/health", async (req, res) => {
    let accounts = 0, marketSymbols = [];
    let keysCount = 0, botsCount = 0;
    try {
        if (db) {
            const aSnap = await db.collection("mt5_accounts").get();
            accounts = aSnap.size;
            const kSnap = await db.collection("prime_keys").get();
            keysCount = kSnap.size;
            const bSnap = await db.collection("prime_bots").get();
            botsCount = bSnap.size;
        }
    } catch(e){ console.log("health error", e); }
    res.json({ 
        status: "ok", 
        uptime: process.uptime(),
        accounts, 
        marketSymbols,
        prime_keys: keysCount,
        prime_bots: botsCount
    });
});

// --- YOUR FLUTTER CALLS THIS - UNTOUCHED ---
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

// =====================================================
// PRIME HOST EA - NEW - START HERE
// =====================================================

function makeKey(){
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let a="", b="";
  for(let i=0;i<4;i++){ a+=chars[Math.floor(Math.random()*chars.length)]; b+=chars[Math.floor(Math.random()*chars.length)]; }
  return `PHE-${a}-${b}`;
}

// 1. CREATE BOT - EA Manager
// POST /prime/bots { name: "THE SHADOW ELITE SCALPER 2.0", pairs: ["GOLD","US30Cash","GER40Cash"], owner: "MT-9994" }
app.post("/prime/bots", async (req, res) => {
  if(!db) return res.status(500).json({error:"No DB"});
  const { name, pairs, owner } = req.body;
  const data = { name, pairs: pairs||[], owner: owner||"MT-9994", created: new Date().toISOString(), status:"Active" };
  const doc = await db.collection("prime_bots").add(data);
  res.json({ success:true, id: doc.id, ...data });
});

app.get("/prime/bots", async (req, res) => {
  if(!db) return res.json([]);
  const snap = await db.collection("prime_bots").get();
  res.json(snap.docs.map(d=>({id:d.id, ...d.data()})));
});

// 2. GENERATE KEY - Keys tab
// POST /prime/keys/generate { username, email, duration_days:30, bot_id, bot_name }
app.post("/prime/keys/generate", async (req, res) => {
  if(!db) return res.status(500).json({error:"No DB"});
  const { username, email, duration_days, bot_id, bot_name } = req.body;
  const code = makeKey();
  const days = Number(duration_days) || 30;
  const expires = new Date(Date.now() + days*24*60*60*1000).toISOString();
  const data = {
    code, username: username||"", email: email||"",
    bot_id: bot_id||"", bot_name: bot_name||"",
    duration_days: days, status: "UNUSED",
    created: new Date().toISOString(), expires
  };
  const doc = await db.collection("prime_keys").add(data);
  res.json({ success:true, id: doc.id, ...data });
});

app.get("/prime/keys", async (req, res) => {
  if(!db) return res.json([]);
  const snap = await db.collection("prime_keys").get();
  res.json(snap.docs.map(d=>({id:d.id, ...d.data()})));
});

// 3. VALIDATE KEY - SlowMo Bizz EA calls this
// GET /keys/validate?key=PHE-XXXX-XXXX
// Also support /prime/keys/validate
app.get(["/keys/validate","/prime/keys/validate"], async (req, res) => {
  const key = (req.query.key || "").trim().toUpperCase();
  if(!key) return res.json({ valid:false, error:"No key" });
  if(!db) return res.json({ valid:false, error:"No DB" });

  const snap = await db.collection("prime_keys").where("code","==",key).get();
  if(snap.empty) return res.json({ valid:false, error:"Key not found" });

  const doc = snap.docs[0];
  const data = doc.data();

  if(data.status === "INACTIVE") return res.json({ valid:false, error:"Key deactivated" });
  if(new Date(data.expires) < new Date()) {
    return res.json({ valid:false, error:"Key expired" });
  }

  // First use -> mark ACTIVE
  if(data.status === "UNUSED"){
    await doc.ref.update({ status:"ACTIVE", activated: new Date().toISOString() });
  }

  res.json({ valid:true, bot: data.bot_name||"SlowMo Bizz", expires: data.expires, email: data.email });
});

// 4. DEACTIVATE / REACTIVATE / DELETE KEY
app.post("/prime/keys/toggle", async (req, res) => {
  if(!db) return res.status(500).json({error:"No DB"});
  const { id, status } = req.body; // status = ACTIVE or INACTIVE
  await db.collection("prime_keys").doc(id).update({ status });
  res.json({ success:true, status });
});

app.delete("/prime/keys/:id", async (req, res) => {
  if(!db) return res.status(500).json({error:"No DB"});
  await db.collection("prime_keys").doc(req.params.id).delete();
  res.json({ success:true });
});

// 5. KEY SHOP ORDER - R100 per key
// POST /prime/orders { qty:2, total:200, buyer_email, proof_url }
app.post("/prime/orders", async (req, res) => {
  if(!db) return res.status(500).json({error:"No DB"});
  const { qty, total, buyer_email, proof_url } = req.body;
  const data = { qty: Number(qty)||1, total: Number(total)||100, buyer_email: buyer_email||"", proof_url: proof_url||"", status:"PENDING", created: new Date().toISOString() };
  const doc = await db.collection("prime_orders").add(data);
  res.json({ success:true, id: doc.id, ...data });
});

app.get("/prime/orders", async (req, res) => {
  if(!db) return res.json([]);
  const snap = await db.collection("prime_orders").get();
  res.json(snap.docs.map(d=>({id:d.id, ...d.data()})));
});

app.post("/prime/orders/:id/approve", async (req, res) => {
  if(!db) return res.status(500).json({error:"No DB"});
  await db.collection("prime_orders").doc(req.params.id).update({ status:"APPROVED", approved: new Date().toISOString() });
  res.json({ success:true });
});

// 6. EA HEARTBEAT - So Prime Host shows Server ONLINE
// POST /prime/heartbeat { key, account, balance, bot }
app.post("/prime/heartbeat", async (req, res) => {
  if(!db) return res.json({ ok:true });
  const { key, account, balance, bot } = req.body;
  await db.collection("prime_heartbeat").doc(String(account||"default")).set({
    key: key||"", account: account||"", balance: balance||0, bot: bot||"SlowMo Bizz",
    lastSeen: new Date().toISOString()
  }, { merge:true });
  res.json({ ok:true, server:"ONLINE" });
});

app.get("/prime/heartbeat", async (req, res) => {
  if(!db) return res.json({ online:false });
  const snap = await db.collection("prime_heartbeat").get();
  res.json(snap.docs.map(d=>({id:d.id, ...d.data()})));
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, '0.0.0.0', () => console.log(`Live on ${PORT}`));
