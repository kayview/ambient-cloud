from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from datetime import datetime, timedelta
import secrets
import json

app = FastAPI(title="Prime Host EA Clone")

LICENSES = {}
PARTNERS = {"PH-ADMIN1": {"owner": "admin", "earnings": 0, "referrals": []}}
PENDING = []
SIGNALS = []
ROBOTS = [
    {"id": 1, "name": "LS ICT Sniper V7", "mentor": "Lesego", "winrate": "78%", "active": 24},
    {"id": 2, "name": "Gold Scalper Pro", "mentor": "Junior", "winrate": "82%", "active": 18},
]

def make_html(title, body):
    return f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body{{margin:0;font-family:Inter,Arial;background:#050A14;color:#fff;}}
.grid-bg{{background:radial-gradient(circle at 50% 0%, #0A1A3A 0%, #050A14 70%); min-height:100vh; padding:20px;}}
.card{{background:linear-gradient(180deg, #0F1F3A 0%, #0A1428 100%);border:1px solid #1E3A5F;border-radius:16px;padding:24px;max-width:420px;margin:40px auto;box-shadow:0 20px 60px rgba(0,150,255,0.15);}}
h1{{font-size:28px; margin:0;}} .blue{{color:#2A9DFF;}}
label{{display:block;margin:14px 0 6px;font-size:13px;color:#A0B4CC;}}
input{{width:100%;padding:14px;background:#050A14;border:1px solid #1E3A5F;border-radius:10px;color:#fff;box-sizing:border-box;}}
.btn{{width:100%;padding:14px;background:linear-gradient(90deg, #1E6FFF, #2ABFFF);border:none;border-radius:10px;color:#fff;font-weight:700;margin-top:18px;cursor:pointer;display:block;text-align:center;text-decoration:none;}}
.small{{font-size:11px;color:#7A8CA6;margin-top:8px;}}
.topbar{{display:flex;justify-content:space-between;padding:14px 20px;background:#050A14;border-bottom:1px solid #111;}}
.badge{{background:#0A1F3A;color:#2ABFFF;border:1px solid #1E4A7A;padding:4px 10px;border-radius:20px;font-size:10px;letter-spacing:1px;}}
.stat{{background:#0A1428;border:1px solid #1E3A5F;border-radius:12px;padding:16px;margin-top:8px;}}
.stat b{{font-size:22px;display:block;}}
</style></head><body><div class="grid-bg">{body}</div></body></html>
"""

@app.get("/", response_class=HTMLResponse)
def landing():
    body = """
<div class="topbar"><b>Prime Host <span class="blue">EA</span></b><a href="/mentor/login" style="color:#fff;text-decoration:none;border:1px solid #333;padding:6px 14px;border-radius:20px;font-size:12px;">Sign in</a></div>
<div style="max-width:900px;margin:40px auto;padding:0 20px;">
<div class="badge">INSTITUTIONAL TRADING INFRASTRUCTURE - ZAR</div>
<h1 style="font-size:42px;line-height:1.1;margin-top:20px;">Your trading edge,<br><span class="blue">always online.</span></h1>
<p style="color:#7A8CA6;line-height:1.6;">Deploy mentor-built robots, scan live markets and execute on connected MT4 or MT5 accounts from one secure platform.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px;">
<a href="/activate" class="btn" style="width:auto;padding:12px 20px;">Open an account</a>
<a href="/download" class="btn" style="width:auto;background:#111;border:1px solid #333;">Download Android</a>
<a href="/mentor/login" class="btn" style="width:auto;background:#111;border:1px solid #333;">Sign in</a>
</div>
<div style="margin-top:40px;background:#0A1428;border:1px solid #1E3A5F;border-radius:16px;padding:20px;">
<h2>Operations overview</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
<div class="stat"><b>24</b>ACTIVE ROBOTS</div>
<div class="stat"><b>128</b>STUDENTS</div>
<div class="stat"><b>18</b>LIVE SESSIONS</div>
<div class="stat"><b>43</b>STRATEGIES</div>
</div>
<div style="margin-top:16px;background:#050A14;border-radius:10px;padding:12px;">Prime Host AI Engine - Signal relay and account connection ready</div>
</div>
</div>
"""
    return make_html("Prime Host EA", body)

@app.get("/activate", response_class=HTMLResponse)
def activate_page():
    body = """
<div><a href="/" style="color:#7A8CA6;text-decoration:none;">Back</a></div>
<div class="card" style="text-align:center;">
<div style="background:#000;width:80px;height:80px;margin:0 auto;border-radius:12px;display:flex;align-items:center;justify-content:center;">PRIME<br>HOST</div>
<h2>Open Prime Host EA</h2>
<p style="color:#7A8CA6;font-size:13px;">Lifetime app access - One-time R500 per email<br>Pay by GoTymebank transfer, then submit application. Owner will approve once proof is received.</p>
<form method="post" action="/activate" style="text-align:left;">
<label>Email</label><input name="email" placeholder="you@example.com" required>
<label>MT Account (MT-1234)</label><input name="mt_id" placeholder="MT-1234" required>
<label>Partner Code (optional)</label><input name="partner_code" placeholder="PH-XXXXXX">
<div class="small">Referred by a Prime Host EA partner? Enter their code here.</div>
<button class="btn" type="submit">Activate</button>
</form>
</div>
"""
    return make_html("Activate", body)

@app.post("/activate")
def do_activate(email: str = Form(...), mt_id: str = Form(...), partner_code: str = Form("")):
    code = f"PH-{secrets.token_hex(3).upper()}"
    PENDING.append({"email": email, "mt_id": mt_id, "partner_code": partner_code, "time": datetime.utcnow().isoformat(), "status": "pending"})
    if partner_code in PARTNERS:
        PARTNERS[partner_code]["referrals"].append(email)
    LICENSES[email] = {"mt_id": mt_id, "partner_code": partner_code, "active": False, "my_code": code}
    return HTMLResponse(make_html("Pending", f"""
<div class="card" style="text-align:center;">
<h2>Application Received</h2>
<p style="color:#7A8CA6;">Email: {email}<br>MT: {mt_id}<br>Your Partner Code: {code}</p>
<p style="font-size:13px;">GoTymebank Details:<br><b>Account: 1234567890<br>Ref: {email}</b><br><br>Upload proof on WhatsApp. Owner will approve within 1 hour.</p>
<a href="/" class="btn">Back to Home</a>
</div>
"""))

@app.get("/mentor/login", response_class=HTMLResponse)
def mentor_login_page():
    body = """
<div><a href="/" style="color:#7A8CA6;text-decoration:none;">Back</a></div>
<div class="card">
<h2>Mentor Portal - Welcome back</h2>
<form method="post" action="/mentor/login" style="margin-top:20px;">
<label>Email</label><input name="email" required>
<label>Password</label><input name="password" type="password" required>
<button class="btn">Login</button>
<div style="text-align:center;margin-top:12px;"><small>Don't have account? <a href="/mentor/register" style="color:#2ABFFF;">Get started</a></small></div>
</form>
</div>
"""
    return make_html("Mentor Login", body)

@app.post("/mentor/login")
def mentor_login(email: str = Form(...), password: str = Form(...)):
    lic = LICENSES.get(email)
    if not lic:
        return HTMLResponse(make_html("Failed", f'<div class="card"><h2>Not found</h2><p>No application for {email}. <a href="/activate">Activate first</a></p></div>'), status_code=401)
    if not lic["active"]:
        return HTMLResponse(make_html("Pending", f'<div class="card"><h2>Awaiting Approval</h2><p>Owner has not approved {email} yet.</p></div>'))
    return RedirectResponse(f"/dashboard?email={email}", status_code=302)

@app.get("/mentor/register", response_class=HTMLResponse)
def mentor_register_page():
    body = """
<div><a href="/" style="color:#7A8CA6;text-decoration:none;">Back</a></div>
<div class="card">
<h2>Mentor Application - Create Account</h2><small style="color:#7A8CA6;">Mentor signup - owner approval required</small>
<form method="post" action="/mentor/register" style="margin-top:16px;">
<label>Username</label><input name="username" required>
<label>Display Name</label><input name="display" required>
<label>Email</label><input name="email" required>
<label>Phone Number</label><input name="phone" required>
<label>Password</label><input name="password" type="password" required>
<label>Partner code (optional)</label><input name="partner_code" placeholder="PH-XXXXXX">
<button class="btn">Register</button>
</form>
</div>
"""
    return make_html("Register", body)

@app.post("/mentor/register")
def mentor_register(username: str = Form(...), display: str = Form(...), email: str = Form(...), phone: str = Form(...), password: str = Form(...), partner_code: str = Form("")):
    return RedirectResponse(f"/activate?email={email}", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(email: str = ""):
    lic = LICENSES.get(email, {})
    robots_html = "".join([f'<div class="stat"><b>{r["name"]}</b><br><small>Mentor: {r["mentor"]} | Winrate: {r["winrate"]}</small><br><button class="btn" style="width:auto;padding:8px 16px;margin-top:8px;">Deploy to MT {lic.get("mt_id","")}</button></div>' for r in ROBOTS])
    return make_html("Dashboard", f"""
<div class="topbar"><b>Prime Host EA</b><small>{email}</small></div>
<div style="max-width:900px;margin:20px auto;padding:20px;">
<h2>Welcome, {email}</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
<div class="stat"><b>{len(ROBOTS)}</b>YOUR ROBOTS</div>
<div class="stat"><b>{lic.get('my_code','PH-XXXXXX')}</b>YOUR PARTNER CODE</div>
</div>
<h3 style="margin-top:24px;">Available Robots</h3>
{robots_html}
<div style="margin-top:20px;" class="stat"><b>Signal Relay: ONLINE</b><br><small>AI Engine connected</small></div>
</div>
""")

@app.get("/verify")
def verify(key: str = "", email: str = ""):
    target = key or email
    lic = LICENSES.get(target)
    if not lic:
        for e, d in LICENSES.items():
            if d.get("mt_id") == target:
                lic = d
                target = e
                break
    if not lic:
        return {"approved": False, "reason": "Invalid key"}
    if not lic.get("active"):
        return {"approved": False, "reason": "Pending approval"}
    return {"approved": True, "email": target, "mt_id": lic.get("mt_id"), "access": "granted", "partner_code": lic.get("my_code")}

@app.post("/api/signal")
async def signal(request: Request):
    data = await request.json()
    data["at"] = datetime.utcnow().isoformat()
    SIGNALS.append(data)
    return {"received": True}

@app.get("/api/signals")
def signals():
    return SIGNALS[-50:]

@app.get("/admin", response_class=HTMLResponse)
def admin():
    pending_html = "".join([f"<div style='border:1px solid #333;padding:10px;margin:6px;border-radius:8px;'><b>{p['email']}</b> MT:{p['mt_id']} Code:{p['partner_code']} <a href='/admin/approve?email={p['email']}' style='color:#0f0;'>[APPROVE]</a> <a href='/admin/deny?email={p['email']}' style='color:#f00;'>[DENY]</a></div>" for p in PENDING if LICENSES.get(p['email'],{}).get('active')==False])
    active_html = "".join([f"<div style='padding:6px;'>{e} - MT {d.get('mt_id')} - Code {d.get('my_code')} - Active: {d.get('active')}</div>" for e,d in LICENSES.items()])
    return make_html("Admin", f"""
<div style="max-width:900px;margin:20px auto;">
<h1>Admin Panel</h1>
<h2>Pending</h2>
{pending_html or '<p>No pending</p>'}
<h2>All Licenses</h2>
{active_html}
</div>
""")

@app.get("/admin/approve")
def approve(email: str):
    if email in LICENSES:
        LICENSES[email]["active"] = True
    return RedirectResponse("/admin")

@app.get("/admin/deny")
def deny(email: str):
    LICENSES.pop(email, None)
    return RedirectResponse("/admin")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/download")
def download():
    return RedirectResponse("/")
