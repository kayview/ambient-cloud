from fastapi import FastAPI, Form, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from datetime import datetime
import json, os, secrets

app = FastAPI(title="BP ICT Engine")

# ===== CONFIG - EDIT THESE =====
BRAND_NAME = "BP ICT Engine"  # <-- Change to your brand
BRAND_SHORT = "BP ICT"
ADMIN_PASSWORD = "bp_admin_2026_secure"  # <-- Change this
GOTYME_BANK = "Account: YOUR_GOTYME_NUMBER | Ref: Your Email"
# ===============================

DB_FILE = "licenses.json"
SIGNALS_FILE = "signals.json"

def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Persistent storage
LICENSES = load_json(DB_FILE, {})
PENDING = load_json("pending.json", [])
SIGNALS = load_json(SIGNALS_FILE, [])
ROBOTS = [
    {"id": 1, "name": "LS ICT Sniper V7.02", "mentor": "Lesego", "winrate": "78%", "tf": "H1/M15/M1", "desc": "Liquidity Sweep + BB/EMA"},
    {"id": 2, "name": "Gold M5 Scalper", "mentor": "BP", "winrate": "74%", "tf": "M5/M1", "desc": "Wick-purge + ATR Trail"},
    {"id": 3, "name": "Breaker Block Pro", "mentor": "BP", "winrate": "81%", "tf": "H1/M15", "desc": "Macro Bias + OB"},
]

PARTNERS = {"BP-ADMIN": {"owner": "admin", "earnings": 0, "referrals": []}}

def make_html(title, body):
    return f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - {BRAND_NAME}</title>
<style>
body{{margin:0;font-family:Inter,system-ui;background:#050A14;color:#fff;}}
.grid-bg{{background:radial-gradient(circle at 50% 0%, #0A1A3A 0%, #050A14 70%);min-height:100vh;}}
.topbar{{display:flex;justify-content:space-between;align-items:center;padding:14px 20px;background:#050A14;border-bottom:1px solid #1A2A4A;position:sticky;top:0;}}
.card{{background:linear-gradient(180deg,#0F1F3A 0%,#0A1428 100%);border:1px solid #1E3A5F;border-radius:16px;padding:24px;max-width:440px;margin:40px auto;box-shadow:0 20px 60px rgba(0,150,255,0.15);}}
h1{{font-size:32px;line-height:1.1;margin:0;}} .blue{{color:#2A9DFF;}}
label{{display:block;margin:14px 0 6px;font-size:13px;color:#A0B4CC;}}
input{{width:100%;padding:14px;background:#050A14;border:1px solid #1E3A5F;border-radius:10px;color:#fff;box-sizing:border-box;}}
.btn{{width:100%;padding:14px;background:linear-gradient(90deg,#1E6FFF,#2ABFFF);border:none;border-radius:10px;color:#fff;font-weight:700;margin-top:18px;cursor:pointer;display:block;text-align:center;text-decoration:none;}}
.btn-dark{{background:#111;border:1px solid #333;}}
.badge{{background:#0A1F3A;color:#2ABFFF;border:1px solid #1E4A7A;padding:4px 10px;border-radius:20px;font-size:10px;letter-spacing:1px;display:inline-block;}}
.stat{{background:#0A1428;border:1px solid #1E3A5F;border-radius:12px;padding:16px;}}
.small{{font-size:11px;color:#7A8CA6;margin-top:8px;line-height:1.4;}}
</style></head><body><div class="grid-bg">{body}</div></body></html>
"""

# ===== LANDING =====
@app.get("/", response_class=HTMLResponse)
def landing():
    body = f"""
<div class="topbar"><b>{BRAND_SHORT} <span class="blue">Engine</span></b><a href="/mentor/login" style="color:#fff;text-decoration:none;border:1px solid #333;padding:6px 14px;border-radius:20px;font-size:12px;">Sign in</a></div>
<div style="max-width:1000px;margin:40px auto;padding:0 20px;">
<div class="badge">INSTITUTIONAL MTF: H1 BIAS / M15 SWEEP / M1 EXECUTION</div>
<h1 style="font-size:44px;margin-top:20px;">Your trading edge,<br><span class="blue">always online.</span></h1>
<p style="color:#7A8CA6;line-height:1.6;max-width:600px;">Deploy mentor-built MTF robots, scan liquidity sweeps, and execute on MT4/MT5 from one secure platform. No VPS.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px;">
<a href="/activate" class="btn" style="width:auto;padding:12px 24px;">Open an Account - R500 Lifetime</a>
<a href="/download" class="btn btn-dark" style="width:auto;padding:12px 20px;">Download Android APK</a>
</div>
<div style="margin-top:40px;background:#0A1428;border:1px solid #1E3A5F;border-radius:16px;padding:24px;">
<h2>Operations Overview</h2>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;">
<div class="stat"><b>{len(ROBOTS)}</b>ACTIVE ROBOTS</div>
<div class="stat"><b>{len(LICENSES)}</b>LICENSED USERS</div>
<div class="stat"><b>{len(SIGNALS)}</b>LIVE SIGNALS</div>
<div class="stat"><b>MTF</b>FRAMEWORK</div>
</div>
<div style="margin-top:16px;background:#050A14;border-radius:10px;padding:14px;font-family:monospace;font-size:12px;color:#2ABFFF;">Engine: H1 Macro (EMA 9/21/200) → M15/M5 Wick Purge → M1 BB Touch + EMA Cross + ATR Trail + Stacking</div>
</div>
</div>
"""
    return make_html("Home", body)

# ===== ACTIVATE =====
@app.get("/activate", response_class=HTMLResponse)
def activate_page():
    body = f"""
<div style="padding:20px;"><a href="/" style="color:#7A8CA6;text-decoration:none;">← Back</a></div>
<div class="card" style="text-align:center;">
<div style="background:#000;width:80px;height:80px;margin:0 auto;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#2ABFFF;">{BRAND_SHORT}</div>
<h2>Open {BRAND_NAME}</h2>
<p class="small">Lifetime app access - One-time R500 per email<br>Pay via GoTymebank, then submit. Admin approves after proof.</p>
<form method="post" action="/activate" style="text-align:left;">
<label>Email</label><input name="email" type="email" placeholder="you@example.com" required>
<label>MT Account (MT-1234 or number)</label><input name="mt_id" placeholder="MT-1234" required>
<label>Partner Code (optional)</label><input name="partner_code" placeholder="BP-XXXXXX">
<div class="small">Referred by partner? Enter code here for commission.</div>
<button class="btn" type="submit">Activate</button>
</form>
<div class="small" style="margin-top:14px;text-align:left;background:#050A14;padding:10px;border-radius:8px;">{GOTYME_BANK}</div>
</div>
"""
    return make_html("Activate", body)

@app.post("/activate")
def do_activate(email: str = Form(...), mt_id: str = Form(...), partner_code: str = Form("")):
    email = email.lower().strip()
    my_code = f"BP-{secrets.token_hex(3).upper()}"
    
    LICENSES[email] = {
        "email": email, "mt_id": mt_id.strip(), "partner_code": partner_code.upper().strip(),
        "my_code": my_code, "active": False, 
        "created": datetime.utcnow().isoformat(),
        "reason": "Pending R500 payment"
    }
    PENDING.append({"email": email, "mt_id": mt_id, "partner_code": partner_code, "time": datetime.utcnow().isoformat()})
    
    save_json(DB_FILE, LICENSES)
    save_json("pending.json", PENDING)
    
    if partner_code.upper() in PARTNERS:
        PARTNERS[partner_code.upper()]["referrals"].append(email)

    return HTMLResponse(make_html("Pending", f"""
<div class="card" style="text-align:center;">
<h2>Application Received ✓</h2>
<p>Email: <b>{email}</b><br>MT: <b>{mt_id}</b><br>Your Partner Code: <b style="color:#2ABFFF">{my_code}</b></p>
<div style="background:#050A14;border:1px solid #1E3A5F;border-radius:10px;padding:12px;margin:16px 0;text-align:left;">
<b>Next Steps:</b><br>1. Pay R500 to GoTymebank<br><b>{GOTYME_BANK}</b><br>Reference: {email}<br>2. Send proof on WhatsApp<br>3. Admin approves in <1 hour
</div>
<a href="/" class="btn">Back to Home</a>
</div>
"""))

# ===== AUTH =====
@app.get("/mentor/login", response_class=HTMLResponse)
def login_page():
    body = """
<div style="padding:20px;"><a href="/" style="color:#7A8CA6;text-decoration:none;">← Back</a></div>
<div class="card">
<h2>Welcome Back</h2>
<p class="small">Enter your approved email</p>
<form method="post" action="/mentor/login" style="margin-top:16px;">
<label>Email</label><input name="email" type="email" required>
<label>Password (any - email is license)</label><input name="password" type="password" required>
<button class="btn">Login to Dashboard</button>
</form>
<div style="text-align:center;margin-top:12px;"><small>Don't have account? <a href="/activate" style="color:#2ABFFF;">Open account</a></small></div>
</div>
"""
    return make_html("Login", body)

@app.post("/mentor/login")
def login(email: str = Form(...), password: str = Form(...)):
    email = email.lower().strip()
    lic = LICENSES.get(email)
    if not lic:
        return HTMLResponse(make_html("Not Found", f'<div class="card"><h2>Email not found</h2><p>{email} not registered. <a href="/activate" style="color:#2ABFFF;">Activate</a></p></div>'), status_code=401)
    if not lic.get("active"):
        return HTMLResponse(make_html("Pending", f'<div class="card"><h2>Awaiting Approval</h2><p>{email} is pending. Send GoTymebank proof. Reason: {lic.get("reason")}</p><a href="/" class="btn">Home</a></div>'))
    return RedirectResponse(f"/dashboard?email={email}", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(email: str = Query("")):
    email = email.lower().strip()
    lic = LICENSES.get(email, {})
    if not lic.get("active"):
        return RedirectResponse("/mentor/login")
    
    robots_html = "".join([f'<div class="stat" style="margin-top:12px;"><b>{r["name"]}</b> <span style="float:right;color:#2ABFFF">{r["winrate"]}</span><br><small style="color:#7A8CA6;">{r["desc"]} | TF: {r["tf"]} | Mentor: {r["mentor"]}</small><br><button class="btn" style="width:auto;padding:8px 16px;margin-top:10px;font-size:12px;">Deploy to MT {lic.get("mt_id","")}</button></div>' for r in ROBOTS])
    
    return make_html("Dashboard", f"""
<div class="topbar"><b>{BRAND_SHORT} Engine</b><small>{email} | {lic.get("my_code")}</small></div>
<div style="max-width:900px;margin:20px auto;padding:20px;">
<h2>Welcome, {email}</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
<div class="stat"><b>{lic.get("my_code")}</b><br><small>YOUR PARTNER CODE</small></div>
<div class="stat"><b>{len(PARTNERS.get(lic.get("my_code"),{}).get("referrals",[]))}</b><br><small>YOUR REFERRALS</small></div>
</div>
<h3 style="margin-top:28px;">Available Robots - MTF Engine</h3>
{robots_html}
<div class="stat" style="margin-top:20px;background:linear-gradient(90deg,#0A1F3A,#0A1428);"><b style="color:#2ABFFF;">● Signal Relay: ONLINE</b><br><small>AI Engine connected | {len(SIGNALS)} signals today</small></div>
</div>
""")

# ===== VERIFY - EA CALLS THIS =====
@app.get("/verify")
def verify(key: str = Query(""), email: str = Query("")):
    target = (key or email).lower().strip()
    if not target:
        return JSONResponse({"approved": False, "reason": "No key"})
    
    # Search by email or MT ID
    found_email = None
    found_data = None
    for e,d in LICENSES.items():
        if e.lower() == target or d.get("mt_id","").lower() == target.lower():
            found_email = e
            found_data = d
            break
    
    if not found_data:
        return JSONResponse({"approved": False, "reason": "Invalid key - not registered"})
    if not found_data.get("active"):
        return JSONResponse({"approved": False, "reason": found_data.get("reason","Pending approval")})
    
    return JSONResponse({
        "approved": True, "email": found_email, "mt_id": found_data.get("mt_id"),
        "access": "granted", "partner_code": found_data.get("my_code"),
        "brand": BRAND_NAME
    })

# ===== SIGNALS =====
@app.post("/api/signal")
async def post_signal(request: Request):
    data = await request.json()
    data["at"] = datetime.utcnow().isoformat()
    SIGNALS.append(data)
    save_json(SIGNALS_FILE, SIGNALS[-200:])
    return {"received": True, "count": len(SIGNALS)}

@app.get("/api/signals")
def get_signals():
    return JSONResponse(SIGNALS[-50:])

# ===== ADMIN - SECURED =====
@app.get("/admin", response_class=HTMLResponse)
def admin_page(password: str = Query("")):
    if password != ADMIN_PASSWORD:
        return HTMLResponse(make_html("Admin Login", f"""
<div class="card"><h2>Admin Access</h2>
<form><label>Admin Password</label><input name="password" type="password" placeholder="{ADMIN_PASSWORD}"><button class="btn">Login</button></form>
<small class="small">Default: {ADMIN_PASSWORD} - Change in code!</small>
</div>
"""))
    
    pending = [p for p in PENDING if not LICENSES.get(p["email"],{}).get("active")]
    pending_html = "".join([f"<div style='border:1px solid #1E3A5F;padding:12px;margin:8px 0;border-radius:10px;background:#0A1428;'><b>{p['email']}</b> | MT: {p['mt_id']} | Partner: {p['partner_code']} | {p['time'][:16]} <br><a href='/admin/approve?email={p['email']}&password={ADMIN_PASSWORD}' style='color:#00FF88;margin-right:12px;'>[APPROVE]</a><a href='/admin/deny?email={p['email']}&password={ADMIN_PASSWORD}' style='color:#FF4444;'>[DENY]</a></div>" for p in pending])
    
    all_html = "".join([f"<div style='padding:6px;border-bottom:1px solid #111;font-size:13px;'>{e} - MT:{d.get('mt_id')} - Code:{d.get('my_code')} - <span style='color:{'#0F0' if d.get('active') else '#FA0'}'>{d.get('active')}</span></div>" for e,d in LICENSES.items()])
    
    return make_html("Admin", f"""
<div style="max-width:1000px;margin:20px auto;padding:20px;">
<h1>{BRAND_NAME} - Admin Panel</h1>
<p class="small">Total licenses: {len(LICENSES)} | Pending: {len(pending)} | Signals: {len(SIGNALS)}</p>
<h2 style="color:#FFAA00;">Pending Approval ({len(pending)})</h2>
{pending_html or "<p>No pending</p>"}
<h2 style="margin-top:30px;">All Licenses</h2>
<div style="background:#0A1428;border:1px solid #1E3A5F;border-radius:10px;padding:10px;max-height:400px;overflow:auto;">{all_html or "None"}</div>
<h2 style="margin-top:30px;">Live Signals</h2>
<div style="background:#050A14;padding:10px;border-radius:10px;font-family:monospace;font-size:11px;">{json.dumps(SIGNALS[-10:], indent=2)}</div>
</div>
""")

@app.get("/admin/approve")
def admin_approve(email: str = Query(""), password: str = Query("")):
    if password != ADMIN_PASSWORD:
        return JSONResponse({"error":"Unauthorized"}, status_code=401)
    email = email.lower().strip()
    if email in LICENSES:
        LICENSES[email]["active"] = True
        LICENSES[email]["reason"] = "Approved - Lifetime Access"
        save_json(DB_FILE, LICENSES)
    return RedirectResponse(f"/admin?password={password}")

@app.get("/admin/deny")
def admin_deny(email: str = Query(""), password: str = Query("")):
    if password != ADMIN_PASSWORD:
        return JSONResponse({"error":"Unauthorized"}, status_code=401)
    email = email.lower().strip()
    LICENSES.pop(email, None)
    save_json(DB_FILE, LICENSES)
    return RedirectResponse(f"/admin?password={password}")

@app.get("/download", response_class=HTMLResponse)
def download_page():
    return make_html("Download", f"""
<div class="card" style="text-align:center;">
<h2>Download {BRAND_NAME}</h2>
<p class="small">Android APK - MTF Engine V7.02</p>
<a href="#" class="btn">Download APK (Add your Drive link here)</a>
<p class="small" style="margin-top:20px;">1. Install APK<br>2. Open account (R500)<br>3. Connect MT4/MT5<br>4. Deploy robot</p>
<a href="/" class="btn btn-dark">Back to Home</a>
</div>
""")

@app.get("/health")
def health():
    return {"ok": True, "brand": BRAND_NAME, "licenses": len(LICENSES), "signals": len(SIGNALS)}
