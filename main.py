from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ambient Host EA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API ---
@app.get("/health")
def health():
    return {"ok": True, "service": "ambient-cloud-2"}

@app.get("/api/stats")
def stats():
    return {
        "robots": 24,
        "students": 128,
        "sessions": 18,
        "strategies": 43
    }

@app.get("/api/robots")
def robots():
    return [
        {"id": "PHE-E78", "name": "KAYVIEW CHARGER", "type": "CHARGER", "status": "active", "expiry": "361d 15h"},
        {"id": "PHE-SNIPER", "name": "SNIPER ELITE", "type": "ENTRY HUNTER", "status": "active"},
    ]

@app.get("/api/market-frameworks")
def frameworks():
    return ["SMC", "ICT", "Price Action", "Support and Resistance", "Supply and Demand", "CRT", "AMD", "PO3"]

# --- FULL WEBSITE ---
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AMBIENT HOST EA - Trading technology. Connected intelligence.</title>
<style>
body{background:#0C0816;color:#fff;font-family:Inter,Arial;margin:0;padding:0}
.container{max-width:1100px;margin:auto;padding:24px}
.hero{border:1px solid #3A2A60;border-radius:24px;background:linear-gradient(180deg,#2A1F45,#0C0816);padding:40px;text-align:center}
.badge{border:1px solid #8B5CF6;color:#8B5CF6;padding:6px 14px;border-radius:20px;font-size:12px}
.btn{background:#8B5CF6;color:#fff;padding:12px 22px;border-radius:20px;text-decoration:none;margin:6px;display:inline-block;font-weight:bold}
.btn2{border:1px solid #fff;color:#fff;padding:12px 22px;border-radius:20px;text-decoration:none;margin:6px;display:inline-block}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;margin-top:20px}
.card{background:#1A1430;border:1px solid #ffffff15;padding:16px;border-radius:16px}
h2{color:#8B5CF6;letter-spacing:1px}
.price{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:700px){.grid{grid-template-columns:1fr 1fr}.price{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="container">
<div style="text-align:center;padding:10px"><b>AMBIENT HOST EA</b><br><small style="color:#999">Trading technology. Connected intelligence.</small></div>

<div class="hero">
<h1>Take control of your trading operations.</h1>
<p style="color:#bbb">One connected environment for automated trading, intelligent market analysis and MT4/MT5 execution. Ambient Host EA brings trading automation and market intelligence together.</p>
<a class="btn" href="#start">GET STARTED</a><a class="btn2" href="#platform">EXPLORE THE PLATFORM</a>
<p style="color:#555;font-size:10px;margin-top:16px">MT4 Compatible · MT5 Compatible · Automated Execution · Multi-Timeframe Analysis</p>
</div>

<h2>THE AMBIENT ECOSYSTEM</h2>
<p>Your trading tools. One environment.</p>
<div class="grid">
<div class="card"><h1 style="color:#8B5CF6;margin:0">24</h1><small>Active trading robots</small></div>
<div class="card"><h1 style="color:#8B5CF6;margin:0">128</h1><small>Registered students</small></div>
<div class="card"><h1 style="color:#8B5CF6;margin:0">18</h1><small>Live trading sessions</small></div>
<div class="card"><h1 style="color:#8B5CF6;margin:0">43</h1><small>Available strategy setups</small></div>
</div>

<h2 id="platform">INTELLIGENCE MEETS AUTOMATION</h2>
<div class="card">
<p><b>Automated Strategy Technology</b> - Access professionally developed Expert Advisors</p>
<p><b>Advanced Market Intelligence</b> - liquidity, market structure, supply and demand, price action</p>
<p><b>Precision Entry Analysis</b> - wick behaviour, structure, entry, SL/TP</p>
<p><b>Account Connectivity</b> - Connect MT4/MT5 to Ambient Host</p>
<p><b>Strategy Management</b> - Mentors distribute systems, manage keys</p>
<p><b>Signal Distribution</b> - Relay signals between charts and accounts</p>
</div>

<h2>MEMBERSHIP OPTIONS</h2>
<div class="price">
<div class="card"><h3>STUDENT ACCESS</h3><h1>R299 / month</h1><p style="font-size:13px;color:#bbb">One active EA access key<br>MT4 and MT5 compatibility<br>Access to market scanner<br>Strategy-based entry signals<br>Proposed TP and SL levels<br>Mentor assistance via WhatsApp</p><a class="btn" href="#">REQUEST STUDENT ACCESS</a></div>
<div class="card" style="border-color:#8B5CF6"><h3>MENTOR ACCESS</h3><h1>R1,499 / month</h1><p style="font-size:13px;color:#bbb">MQL4 and MQL5 EA development tools<br>Student key creation and management<br>Client approval controls<br>Hosted and self-hosted client management<br>Payment verification workflow<br>Mentor dashboard<br>Analytics</p><a class="btn" href="#">APPLY FOR MENTOR ACCESS</a></div>
</div>

<h2 id="start">GETTING STARTED</h2>
<div class="card" style="font-size:13px;line-height:1.8;color:#bbb">
01 — Create your profile<br>
02 — Get authorised - mentor provides PHE key<br>
03 — Install trading software - Download MT4/MT5 EA<br>
04 — Connect terminal - Enter key + WebRequest<br>
05 — Access dashboard - Confirm connection<br>
06 — Analyse and execute
</div>

<h2>MARKET CONCEPTS & STRATEGY FRAMEWORKS</h2>
<div class="card" style="color:#bbb;font-size:13px">Smart Money Concepts (SMC)<br>Inner Circle Trader (ICT)<br>Price Action<br>Support and Resistance<br>Supply and Demand<br>Change in Range / CRT<br>Accumulation, Manipulation and Distribution (AMD)<br>Power of Three (PO3)</div>

<h2>ABOUT AMBIENT HOST</h2>
<div class="card" style="color:#bbb;font-size:13px">
Technology developed around the trader.<br><br>
Ambient Host EA is a trading technology initiative established by Kayview Trader, founder of Kayview Traders.<br><br>
Founded by: Kayview Trader<br>Organisation: Kayview Traders<br>Platform: Ambient Host EA<br>Mission: Building smarter connections between traders, strategies and technology.
</div>

<p style="color:#ff5555;font-size:10px;margin-top:30px;border:1px solid #ff555533;padding:12px;border-radius:12px">IMPORTANT: Trading forex, gold and leveraged instruments involves substantial risk. Automated trading does not guarantee profits. Always test on demo.</p>

<div style="text-align:center;padding:30px;color:#666;font-size:11px">© 2026 Ambient Host EA. All rights reserved.<br>Powered by the vision of Kayview Traders.</div>

</div>
</body>
</html>
    """
