from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
import os
import json
import uuid
import uvicorn
from datetime import datetime, timedelta
from urllib.parse import parse_qs

app = FastAPI(
    title="AMERICO AI",
    description="AMERICO AI WEB PRO ADMIN - CENTENO AI API Platform",
    version="4.4.0"
)

SITE_URL = os.getenv("SITE_URL", "https://americo-ai-web.onrender.com")
APP_LINK = os.getenv("APP_LINK", "https://centeno-ai-pro.base44.app")

WHATSAPP_LINK = "https://wa.me/51905917699"
MAIN_EMAIL = "centenocolqueg@gmail.com"
FOUNDER = "G. Americo Centeno Colque"
COMPANY = "AMERICO AI"
PRODUCT = "CENTENO AI"
API_BASE_URL = os.getenv("API_BASE_URL", "https://mis-apis-americo-jm2e.onrender.com")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "centenocolqueg@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123456")
ADMIN_SESSION = os.getenv("ADMIN_SESSION", "americo_ai_admin_session_2026")

APIS_FILE = "apis.json"
API_KEYS_FILE = "api_keys.json"

COMPANY_HTML = '<span class="notranslate" translate="no">AMERICO AI</span>'
PRODUCT_HTML = '<span class="notranslate" translate="no">CENTENO AI</span>'

API_KEY_PLANS = {
    "centeno_api_starter": {"name": "API Starter", "price": "S/20", "days": 30, "limit": 1000},
    "centeno_api_developer": {"name": "API Developer", "price": "S/50", "days": 30, "limit": 5000},
    "centeno_api_business": {"name": "API Business", "price": "S/100", "days": 30, "limit": 20000},
    "centeno_api_enterprise": {"name": "API Enterprise", "price": "Custom", "days": 30, "limit": 100000}
}


def default_apis():
    return [
        {
            "name": "Text Intelligence API",
            "description": "API oficial para respuestas inteligentes de texto en apps, webs, bots y sistemas empresariales.",
            "endpoint": "/api/texto-app",
            "price": "S/20",
            "product_id": "centeno_api_starter",
            "type": "texto",
            "status": "activa"
        },
        {
            "name": "Image Generation API",
            "description": "API para generar imágenes con inteligencia artificial desde prompts de texto.",
            "endpoint": "/api/imagen",
            "price": "S/50",
            "product_id": "centeno_api_developer",
            "type": "imagen",
            "status": "activa"
        },
        {
            "name": "User Sync API",
            "description": "API para sincronizar usuarios, planes, estados, vencimientos y accesos.",
            "endpoint": "/api/usuario/sync",
            "price": "S/100",
            "product_id": "centeno_api_business",
            "type": "business",
            "status": "activa"
        },
        {
            "name": "History API",
            "description": "API para consultar historial de usuarios, conversaciones, respuestas e imágenes.",
            "endpoint": "/api/historial",
            "price": "S/100",
            "product_id": "centeno_api_business",
            "type": "business",
            "status": "activa"
        }
    ]


def load_apis():
    if not os.path.exists(APIS_FILE):
        save_apis(default_apis())

    try:
        with open(APIS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else default_apis()
    except Exception:
        return default_apis()


def save_apis(apis):
    with open(APIS_FILE, "w", encoding="utf-8") as f:
        json.dump(apis, f, indent=4, ensure_ascii=False)


def load_api_keys():
    if not os.path.exists(API_KEYS_FILE):
        save_api_keys([])

    try:
        with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_api_keys(keys):
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(keys, f, indent=4, ensure_ascii=False)


def is_admin(request: Request):
    return request.cookies.get("admin_session") == ADMIN_SESSION


def generate_real_api_key():
    return "americo_sk_" + uuid.uuid4().hex + uuid.uuid4().hex[:16]


def now_iso():
    return datetime.utcnow().isoformat() + "Z"


def add_days_iso(days: int):
    return (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"


def is_key_active(key_data):
    if key_data.get("status") != "active":
        return False

    expires_at = key_data.get("expires_at", "")
    if not expires_at:
        return False

    try:
        return datetime.utcnow() < datetime.fromisoformat(expires_at.replace("Z", ""))
    except Exception:
        return False


def verify_real_api_key(api_key: str):
    keys = load_api_keys()

    for item in keys:
        if item.get("api_key") == api_key:
            if not is_key_active(item):
                return False, "API Key vencida o inactiva", None

            limit = int(item.get("monthly_limit", 0))
            used = int(item.get("used", 0))

            if used >= limit:
                return False, "Límite mensual agotado", item

            item["used"] = used + 1
            item["updated_at"] = now_iso()
            save_api_keys(keys)

            return True, "API Key válida", item

    return False, "API Key no encontrada", None


def page_style():
    return """
    <style>
      * { box-sizing: border-box; scroll-behavior: smooth; }
      body {
        margin: 0;
        font-family: Inter, Arial, Helvetica, sans-serif;
        background: #030712;
        color: white;
        overflow-x: hidden;
      }
      .notranslate { unicode-bidi: isolate; }
      nav {
        position: sticky;
        top: 0;
        z-index: 50;
        background: rgba(3, 7, 18, 0.94);
        backdrop-filter: blur(18px);
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding: 16px 8%;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .logo { font-size: 24px; font-weight: 950; letter-spacing: 2px; }
      nav a {
        color: #d9ddff;
        text-decoration: none;
        margin-left: 18px;
        font-size: 14px;
        font-weight: 800;
      }
      nav a:hover { color: #d4af37; }
      header {
        min-height: 92vh;
        padding: 90px 8% 70px;
        display: grid;
        grid-template-columns: 1.15fr 0.85fr;
        align-items: center;
        gap: 45px;
        background:
          radial-gradient(circle at 20% 20%, rgba(212,175,55,0.22), transparent 30%),
          radial-gradient(circle at 80% 30%, rgba(59,130,246,0.18), transparent 34%),
          radial-gradient(circle at 50% 90%, rgba(168,85,247,0.14), transparent 38%),
          #030712;
      }
      .badge {
        display: inline-block;
        padding: 10px 16px;
        border-radius: 999px;
        background: rgba(212,175,55,0.13);
        border: 1px solid rgba(212,175,55,0.45);
        color: #f8df7a;
        font-weight: 900;
        margin-bottom: 22px;
        letter-spacing: 1.2px;
        font-size: 13px;
      }
      h1 {
        font-size: clamp(50px, 8vw, 96px);
        line-height: 0.95;
        margin: 0;
        letter-spacing: -3px;
      }
      h2 {
        font-size: clamp(32px, 5vw, 56px);
        margin-bottom: 14px;
        color: #f7f7fb;
        letter-spacing: -1.5px;
      }
      h3 { font-size: 22px; margin-top: 0; }
      p, li { color: #d9ddff; line-height: 1.7; font-size: 18px; }
      .gradient {
        background: linear-gradient(90deg, #d4af37, #8affd2, #8ab4ff);
        -webkit-background-clip: text;
        color: transparent;
      }
      .slogan {
        font-size: 23px;
        color: #d4af37;
        margin: 18px 0;
        max-width: 900px;
        font-weight: 950;
        letter-spacing: 1px;
      }
      .hero-text { max-width: 760px; margin: 20px 0; }
      .btn {
        display: inline-block;
        margin: 10px 8px 10px 0;
        padding: 15px 24px;
        border-radius: 16px;
        background: linear-gradient(90deg, #d4af37, #f59e0b);
        color: #030712;
        text-decoration: none;
        font-weight: 950;
        box-shadow: 0 14px 35px rgba(212,175,55,0.22);
        border: none;
        cursor: pointer;
      }
      .btn.secondary {
        background: rgba(255,255,255,0.08);
        color: white;
        border: 1px solid rgba(255,255,255,0.16);
        box-shadow: none;
      }
      .btn.green { background: linear-gradient(90deg, #10b981, #06b6d4); color: white; }
      .btn.red { background: linear-gradient(90deg, #ef4444, #f97316); color: white; }
      .hero-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.11), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 34px;
        padding: 28px;
        box-shadow: 0 0 80px rgba(212,175,55,0.12);
      }
      .terminal {
        background: #07111f;
        border-radius: 24px;
        padding: 24px;
        color: #8affd2;
        font-family: Consolas, monospace;
        line-height: 1.9;
        font-size: 15px;
        border: 1px solid rgba(138,255,210,0.14);
      }
      section { padding: 75px 8%; max-width: 1250px; margin: auto; }
      .section-subtitle { max-width: 900px; color: #bdc5ee; }
      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(245px, 1fr));
        gap: 22px;
        margin-top: 30px;
      }
      .card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 28px;
        padding: 26px;
        box-shadow: 0 0 35px rgba(124,92,255,0.10);
      }
      .highlight {
        background: linear-gradient(180deg, rgba(212,175,55,0.16), rgba(59,130,246,0.07));
        border: 1px solid rgba(212,175,55,0.38);
      }
      .success {
        background: linear-gradient(180deg, rgba(16,185,129,0.18), rgba(6,182,212,0.08));
        border: 1px solid rgba(16,185,129,0.45);
      }
      .price { font-size: 34px; font-weight: 950; color: white; margin: 10px 0; }
      code {
        display: block;
        padding: 14px;
        border-radius: 14px;
        background: #0b1220;
        color: #8affd2;
        overflow-x: auto;
        margin-top: 12px;
        font-size: 14px;
        border: 1px solid rgba(138,255,210,0.16);
      }
      .status {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(212,175,55,0.13);
        color: #f8df7a;
        font-size: 12px;
        font-weight: 950;
        margin-bottom: 12px;
      }
      .form-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 26px;
        padding: 26px;
        max-width: 780px;
      }
      input, textarea, select {
        width: 100%;
        margin: 8px 0 16px;
        padding: 14px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.18);
        background: #0b1220;
        color: white;
        font-size: 16px;
      }
      label { font-weight: 900; color: #d9ddff; }
      table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background: rgba(255,255,255,0.04);
        border-radius: 20px;
        overflow: hidden;
      }
      th, td {
        padding: 14px;
        border-bottom: 1px solid rgba(255,255,255,0.10);
        color: #d9ddff;
        text-align: left;
        vertical-align: top;
        font-size: 14px;
      }
      th { color: #f8df7a; font-weight: 950; }
      footer {
        text-align: center;
        padding: 42px 22px;
        background: #03050f;
        color: #9aa3cc;
        border-top: 1px solid rgba(255,255,255,0.08);
      }
      a { color: #8affd2; }
      @media (max-width: 850px) {
        nav { flex-direction: column; gap: 12px; }
        nav a { margin: 0 7px; font-size: 13px; }
        header { grid-template-columns: 1fr; padding: 70px 22px; text-align: center; }
      }
    </style>
    """


def nav_html(admin=False):
    if admin:
        extra = '<a href="/admin">Admin</a> <a href="/admin/api-keys">API Keys reales</a> <a href="/admin/logout">Salir</a>'
    else:
        extra = ""

    return f"""
    <nav>
      <div class="logo">{COMPANY_HTML}</div>
      <div>
        <a href="/#centeno">{PRODUCT_HTML}</a>
        <a href="/#api">API Platform</a>
        <a href="/#developer">API Keys</a>
        <a href="/#business">Business</a>
        <a href="/terms">Términos</a>
        <a href="/privacy">Privacidad</a>
        <a href="/support">Soporte</a>
        {extra}
      </div>
    </nav>
    """


def render_api_cards():
    apis = load_apis()
    cards = ""

    for api in apis:
        status = api.get("status", "activa").lower().strip()

        if status not in ["activa", "activo", "active"]:
            continue

        cards += f"""
        <div class="card highlight">
          <span class="status">{api.get("type", "developer").upper()} · API KEY REQUIRED</span>
          <h3>{api.get("name", "API")}</h3>
          <p>{api.get("description", "")}</p>
          <code>{api.get("endpoint", "")}</code>
          <p><strong>Precio:</strong> {api.get("price", "")}</p>
          <p><strong>Product ID Google Billing:</strong> {api.get("product_id", "")}</p>
          <p><strong>Authentication:</strong> x-api-key</p>
          <a class="btn" href="{APP_LINK}">Abrir app y obtener API Key</a>
        </div>
        """

    if not cards:
        cards = """
        <div class="card">
          <h3>No hay APIs activas</h3>
          <p>El administrador todavía no registró APIs disponibles.</p>
        </div>
        """

    return cards


@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="google-site-verification" content="Yo8quOlHsL7cWc6XoIUlURZ_Il6twMGgtK_35PFGhBg" />
  <meta name="google" content="notranslate">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AMERICO AI | CENTENO AI | API Keys with Google Play Billing</title>
  <meta name="description" content="AMERICO AI builds CENTENO AI, AI apps, API Keys, AI chat, image generation, developer APIs and enterprise automation.">
  <meta name="keywords" content="AMERICO AI, CENTENO AI, AI API, API Key, Google Play Billing, artificial intelligence, image generation, automation, developer API">
  <meta name="author" content="{FOUNDER}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE_URL}">
  {page_style()}
</head>
<body>
{nav_html()}

<header>
  <div>
    <div class="badge">OFFICIAL AI TECHNOLOGY COMPANY</div>
    <h1>Building AI for <span class="gradient">Creation, Vision and Code.</span></h1>
    <div class="slogan">{COMPANY_HTML}</div>
    <p class="hero-text">
      {COMPANY_HTML} builds artificial intelligence products, API platforms, automation systems,
      AI assistants, image generation tools and developer solutions for people, businesses and creators.
    </p>
    <a class="btn" href="{APP_LINK}">Open {PRODUCT_HTML} App</a>
    <a class="btn secondary" href="#api">Explore API Platform</a>
    <a class="btn secondary" href="{APP_LINK}">Get API Key</a>
  </div>

  <div class="hero-card">
    <div class="terminal">
      &gt; <span class="notranslate" translate="no">AMERICO AI</span> initialized<br>
      &gt; <span class="notranslate" translate="no">CENTENO AI</span> online<br>
      &gt; Text Intelligence API active<br>
      &gt; Image Generation API active<br>
      &gt; Google Play Billing prepared<br>
      &gt; API Key generator active<br>
      &gt; Admin access hidden<br>
      &gt; App deep link active: centenoai://open<br>
      &gt; Founder & CEO: {FOUNDER}
    </div>
  </div>
</header>

<section id="centeno">
  <h2>{PRODUCT_HTML}</h2>
  <p class="section-subtitle">
    {PRODUCT_HTML} is the official AI application of {COMPANY_HTML}. It is designed for intelligent chat,
    image generation, programming assistance, automation, APIs, projects, history and digital productivity.
  </p>

  <div class="card highlight">
    <h3>Official App</h3>
    <p>
      {PRODUCT_HTML} is the official Android app where users can chat with AI, generate images,
      organize projects, manage history, buy premium plans and buy API Key access.
      Payments are processed securely inside the app using Google Play Billing.
    </p>
    <a class="btn" href="{APP_LINK}">Open {PRODUCT_HTML} App</a>
    <a class="btn secondary" href="/terms">Terms</a>
    <a class="btn secondary" href="/privacy">Privacy</a>
    <a class="btn green" href="{WHATSAPP_LINK}" target="_blank">WhatsApp Support</a>
  </div>
</section>

<section id="api">
  <h2>{PRODUCT_HTML} API Platform</h2>
  <p class="section-subtitle">
    APIs created by {COMPANY_HTML} appear here automatically when the admin registers them.
    Companies and developers must get an API Key inside {PRODUCT_HTML} using Google Play Billing.
  </p>

  <div class="card success">
    <span class="status">API KEY ACCESS FLOW</span>
    <h3>How companies and developers get an API Key</h3>
    <p>
      User opens {PRODUCT_HTML}, selects an API Key plan, pays with Google Play Billing,
      activates the API Key and uses it in their own app, website or business system.
    </p>
    <code>Open CENTENO AI → API Keys → Choose Plan → Pay with Google Play Billing → Activate API Key → Use API</code>
    <a class="btn green" href="{APP_LINK}">Get API Key in {PRODUCT_HTML}</a>
  </div>

  <div class="card highlight">
    <h3>API Base URL</h3>
    <code>{API_BASE_URL}</code>
    <p>Every request requires a valid API Key purchased and activated through {PRODUCT_HTML}.</p>
  </div>

  <div class="grid">
    {render_api_cards()}
  </div>
</section>

<section id="developer">
  <h2>Developer API Keys</h2>
  <p class="section-subtitle">
    Developers and companies obtain API Keys from {PRODUCT_HTML}. API Key plans are paid inside the Android app
    using Google Play Billing.
  </p>

  <div class="grid">
    <div class="card">
      <h3>Step 1 — Open {PRODUCT_HTML}</h3>
      <p>Open the official Android app from this website using the secure app link.</p>
      <a class="btn" href="{APP_LINK}">Open {PRODUCT_HTML}</a>
    </div>
    <div class="card">
      <h3>Step 2 — Choose API Key Plan</h3>
      <p>Select API Starter, API Developer, API Business or Enterprise.</p>
    </div>
    <div class="card">
      <h3>Step 3 — Pay with Google Play Billing</h3>
      <p>Complete the payment securely using Google Play Billing inside {PRODUCT_HTML}.</p>
      <code>centeno_api_starter / centeno_api_developer / centeno_api_business / centeno_api_enterprise</code>
    </div>
    <div class="card highlight">
      <h3>Step 4 — Use the API</h3>
      <p>Use your private API Key in your app, website or business system.</p>
      <code>curl -H "x-api-key: YOUR_API_KEY" {API_BASE_URL}/api/texto-app</code>
    </div>
  </div>
</section>

<section id="business">
  <h2>API Key Plans for Developers and Businesses</h2>
  <p class="section-subtitle">
    API Key access is purchased inside {PRODUCT_HTML} with Google Play Billing.
  </p>

  <div class="grid">
    <div class="card">
      <span class="status">API KEY PLAN</span>
      <h3>API Starter</h3>
      <div class="price">S/20</div>
      <p>For testing, small apps and personal projects.</p>
      <p>Product ID: <strong>centeno_api_starter</strong></p>
      <a class="btn" href="{APP_LINK}">Buy in {PRODUCT_HTML}</a>
    </div>
    <div class="card highlight">
      <span class="status">API KEY PLAN</span>
      <h3>API Developer</h3>
      <div class="price">S/50</div>
      <p>For apps, websites and automation projects.</p>
      <p>Product ID: <strong>centeno_api_developer</strong></p>
      <a class="btn" href="{APP_LINK}">Buy in {PRODUCT_HTML}</a>
    </div>
    <div class="card">
      <span class="status">API KEY PLAN</span>
      <h3>API Business</h3>
      <div class="price">S/100</div>
      <p>For businesses that need AI integrations and higher usage.</p>
      <p>Product ID: <strong>centeno_api_business</strong></p>
      <a class="btn" href="{APP_LINK}">Buy in {PRODUCT_HTML}</a>
    </div>
    <div class="card">
      <span class="status">API KEY PLAN</span>
      <h3>API Enterprise</h3>
      <div class="price">Custom</div>
      <p>For companies that need larger access or private integration.</p>
      <p>Product ID: <strong>centeno_api_enterprise</strong></p>
      <a class="btn" href="{APP_LINK}">Open {PRODUCT_HTML}</a>
    </div>
  </div>
</section>

<section id="legal">
  <h2>Legal Documents</h2>
  <div class="grid">
    <div class="card">
      <h3>Terms of Service</h3>
      <p>Terms and conditions for using {PRODUCT_HTML} and {COMPANY_HTML} services.</p>
      <a class="btn" href="/terms">Open Terms</a>
    </div>
    <div class="card">
      <h3>Privacy Policy</h3>
      <p>Privacy policy for user data, history, projects, subscriptions and API Keys.</p>
      <a class="btn" href="/privacy">Open Privacy</a>
    </div>
    <div class="card">
      <h3>Support</h3>
      <p>Official support for {PRODUCT_HTML} and {COMPANY_HTML}.</p>
      <a class="btn green" href="/support">Open Support</a>
    </div>
  </div>
</section>

<section id="contact">
  <h2>Contact {COMPANY_HTML}</h2>
  <p>WhatsApp Support:<br><a href="{WHATSAPP_LINK}">+51 905 917 699</a></p>
  <p>Main Email: {MAIN_EMAIL}</p>
  <p>
    For {PRODUCT_HTML} access, API Key access, enterprise integrations, developer access or business support,
    open {PRODUCT_HTML} or contact {COMPANY_HTML} through WhatsApp or main email.
  </p>
</section>

<footer>
  © 2026 {COMPANY_HTML} — Building Artificial Intelligence for Creation, Vision and Code.
</footer>

</body>
</html>
"""


@app.get("/open-app")
def open_app():
    return RedirectResponse(APP_LINK, status_code=302)


@app.post("/api/key/activar")
async def activar_api_key(request: Request):
    try:
        data = await request.json()
    except Exception:
        return {"ok": False, "error": "JSON inválido"}

    email = str(data.get("email", "")).strip().lower()
    product_id = str(data.get("product_id", "")).strip()
    purchase_token = str(data.get("purchase_token", "")).strip()

    if not email or "@" not in email:
        return {"ok": False, "error": "Correo inválido"}

    if product_id not in API_KEY_PLANS:
        return {"ok": False, "error": "Plan API Key inválido"}

    plan = API_KEY_PLANS[product_id]
    keys = load_api_keys()
    existing = None

    for item in keys:
        if item.get("email", "").lower() == email and item.get("product_id") == product_id and item.get("status") == "active":
            existing = item
            break

    if existing:
        existing["expires_at"] = add_days_iso(plan["days"])
        existing["updated_at"] = now_iso()
        existing["purchase_token"] = purchase_token
        api_key = existing["api_key"]
    else:
        api_key = generate_real_api_key()
        keys.append({
            "email": email,
            "api_key": api_key,
            "product_id": product_id,
            "plan_name": plan["name"],
            "price": plan["price"],
            "monthly_limit": plan["limit"],
            "used": 0,
            "status": "active",
            "purchase_token": purchase_token,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "expires_at": add_days_iso(plan["days"])
        })

    save_api_keys(keys)

    return {
        "ok": True,
        "message": "API Key activada correctamente",
        "email": email,
        "product_id": product_id,
        "plan_name": plan["name"],
        "api_key": api_key,
        "monthly_limit": plan["limit"],
        "expires_at": add_days_iso(plan["days"])
    }


@app.get("/api/key/mis-keys")
def mis_api_keys(email: str):
    email = email.strip().lower()
    keys = load_api_keys()
    user_keys = []

    for item in keys:
        if item.get("email", "").lower() == email:
            safe_item = dict(item)
            safe_item["active"] = is_key_active(item)
            user_keys.append(safe_item)

    return {"ok": True, "email": email, "total": len(user_keys), "keys": user_keys}


@app.get("/api/key/admin/todas")
def todas_api_keys(request: Request):
    if not is_admin(request):
        return {"ok": False, "error": "No autorizado"}

    keys = load_api_keys()
    return {"ok": True, "total": len(keys), "keys": keys}


@app.get("/api/key/probar")
def probar_api_key(request: Request):
    api_key = request.headers.get("x-api-key", "").strip()

    if not api_key:
        return {"ok": False, "error": "Falta header x-api-key"}

    valid, message, data = verify_real_api_key(api_key)

    if not valid:
        return {"ok": False, "error": message}

    return {
        "ok": True,
        "message": message,
        "email": data.get("email"),
        "plan": data.get("plan_name"),
        "used": data.get("used"),
        "monthly_limit": data.get("monthly_limit")
    }


@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_page():
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Admin Login | AMERICO AI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {page_style()}
</head>
<body>
<section>
  <h2>Panel Admin Privado</h2>
  <p class="section-subtitle">Acceso privado para administrar APIs y API Keys reales de AMERICO AI.</p>

  <div class="form-box">
    <form method="post" action="/admin/login">
      <label>Email admin</label>
      <input type="email" name="email" placeholder="Correo admin" required>

      <label>Contraseña</label>
      <input type="password" name="password" placeholder="Contraseña admin" required>

      <button class="btn green" type="submit">Entrar</button>
      <a class="btn secondary" href="/">Volver</a>
    </form>
  </div>
</section>
</body>
</html>
"""


@app.post("/admin/login")
async def admin_login(request: Request):
    body = await request.body()
    data = parse_qs(body.decode("utf-8"))

    email = data.get("email", [""])[0].strip().lower()
    password = data.get("password", [""])[0].strip()

    if email == ADMIN_EMAIL.lower() and password == ADMIN_PASSWORD:
        response = RedirectResponse("/admin", status_code=302)
        response.set_cookie(
            key="admin_session",
            value=ADMIN_SESSION,
            httponly=True,
            max_age=60 * 60 * 24
        )
        return response

    return HTMLResponse("""
    <body style="background:#050816;color:white;font-family:Arial;padding:40px;">
      <h1>Acceso denegado</h1>
      <p>Email o contraseña incorrectos.</p>
      <a style="color:#8affd2;" href="/admin/login">Volver</a>
    </body>
    """, status_code=401)


@app.get("/admin/logout")
def admin_logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("admin_session")
    return response


@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request):
    if not is_admin(request):
        return RedirectResponse("/admin/login", status_code=302)

    apis = load_apis()
    rows = ""

    for index, api in enumerate(apis):
        rows += f"""
        <div class="card">
          <span class="status">{api.get("status", "activa").upper()}</span>
          <h3>{api.get("name", "API")}</h3>
          <p>{api.get("description", "")}</p>
          <code>{api.get("endpoint", "")}</code>
          <p><strong>Precio:</strong> {api.get("price", "")}</p>
          <p><strong>Product ID:</strong> {api.get("product_id", "")}</p>
          <p><strong>Tipo:</strong> {api.get("type", "")}</p>
          <a class="btn red" href="/admin/apis/delete/{index}" onclick="return confirm('¿Eliminar esta API?')">Eliminar</a>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Admin | AMERICO AI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {page_style()}
</head>
<body>
{nav_html(admin=True)}

<section>
  <h2>Panel Admin APIs</h2>
  <p class="section-subtitle">
    Admin: {ADMIN_EMAIL}. Aquí registras las APIs creadas por ti para que aparezcan en tu página empresarial.
  </p>

  <a class="btn green" href="/admin/apis/new">Agregar nueva API</a>
  <a class="btn secondary" href="/admin/api-keys">Ver API Keys reales</a>
  <a class="btn secondary" href="/">Ver página pública</a>
  <a class="btn red" href="/admin/logout">Cerrar sesión</a>

  <div class="grid">
    {rows}
  </div>
</section>

</body>
</html>
"""


@app.get("/admin/api-keys", response_class=HTMLResponse)
def admin_api_keys_page(request: Request):
    if not is_admin(request):
        return RedirectResponse("/admin/login", status_code=302)

    keys = load_api_keys()
    rows = ""

    if not keys:
        rows = '<tr><td colspan="8">Todavía no hay API Keys generadas.</td></tr>'
    else:
        for item in keys:
            active = "ACTIVA" if is_key_active(item) else "INACTIVA/VENCIDA"
            api_key = item.get("api_key", "")
            api_key_short = api_key[:22] + "..." if len(api_key) > 22 else api_key

            rows += f"""
            <tr>
              <td>{item.get("email", "")}</td>
              <td>{item.get("plan_name", "")}</td>
              <td>{item.get("product_id", "")}</td>
              <td>{api_key_short}</td>
              <td>{item.get("used", 0)} / {item.get("monthly_limit", 0)}</td>
              <td>{active}</td>
              <td>{item.get("expires_at", "")}</td>
              <td>{item.get("created_at", "")}</td>
            </tr>
            """

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>API Keys Reales | AMERICO AI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {page_style()}
</head>
<body>
{nav_html(admin=True)}

<section>
  <h2>API Keys Reales</h2>
  <p class="section-subtitle">
    Aquí aparecen las claves reales generadas cuando un usuario compra o activa un plan API Key.
  </p>

  <a class="btn secondary" href="/admin">Volver al admin</a>
  <a class="btn secondary" href="/api/key/admin/todas">Ver JSON</a>

  <table>
    <thead>
      <tr>
        <th>Email</th>
        <th>Plan</th>
        <th>Product ID</th>
        <th>API Key</th>
        <th>Uso</th>
        <th>Estado</th>
        <th>Vence</th>
        <th>Creada</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</section>

</body>
</html>
"""


@app.get("/admin/apis/new", response_class=HTMLResponse)
def new_api_page(request: Request):
    if not is_admin(request):
        return RedirectResponse("/admin/login", status_code=302)

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Nueva API | AMERICO AI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {page_style()}
</head>
<body>
{nav_html(admin=True)}

<section>
  <h2>Agregar nueva API</h2>
  <p class="section-subtitle">Esta API aparecerá automáticamente en la página pública de {COMPANY_HTML}.</p>

  <div class="form-box">
    <form method="post" action="/admin/apis/new">
      <label>Nombre de API</label>
      <input name="name" placeholder="Ejemplo: Text Intelligence API" required>

      <label>Descripción</label>
      <textarea name="description" rows="5" placeholder="Describe para qué sirve esta API" required></textarea>

      <label>Endpoint</label>
      <input name="endpoint" placeholder="/api/texto-app" required>

      <label>Precio</label>
      <input name="price" placeholder="S/20" required>

      <label>Product ID Google Billing</label>
      <input name="product_id" placeholder="centeno_api_starter" required>

      <label>Tipo</label>
      <select name="type">
        <option value="texto">texto</option>
        <option value="imagen">imagen</option>
        <option value="business">business</option>
        <option value="developer">developer</option>
        <option value="enterprise">enterprise</option>
      </select>

      <label>Estado</label>
      <select name="status">
        <option value="activa">activa</option>
        <option value="apagada">apagada</option>
      </select>

      <button class="btn green" type="submit">Guardar API</button>
      <a class="btn secondary" href="/admin">Cancelar</a>
    </form>
  </div>
</section>

</body>
</html>
"""


@app.post("/admin/apis/new")
async def create_api(request: Request):
    if not is_admin(request):
        return RedirectResponse("/admin/login", status_code=302)

    body = await request.body()
    data = parse_qs(body.decode("utf-8"))

    api = {
        "name": data.get("name", [""])[0].strip(),
        "description": data.get("description", [""])[0].strip(),
        "endpoint": data.get("endpoint", [""])[0].strip(),
        "price": data.get("price", [""])[0].strip(),
        "product_id": data.get("product_id", [""])[0].strip(),
        "type": data.get("type", ["developer"])[0].strip(),
        "status": data.get("status", ["activa"])[0].strip()
    }

    apis = load_apis()
    apis.append(api)
    save_apis(apis)

    return RedirectResponse("/admin", status_code=302)


@app.get("/admin/apis/delete/{index}")
def delete_api(index: int, request: Request):
    if not is_admin(request):
        return RedirectResponse("/admin/login", status_code=302)

    apis = load_apis()

    if 0 <= index < len(apis):
        apis.pop(index)
        save_apis(apis)

    return RedirectResponse("/admin", status_code=302)


def legal_page(title: str, content: str):
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="google" content="notranslate">
  <title>{title} | CENTENO AI</title>
  <meta name="robots" content="index, follow">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {page_style()}
</head>
<body>
{nav_html()}
<section>
  <h2>{title}</h2>
  <div class="card">
    {content}
    <br>
    <a class="btn secondary" href="/">Volver a {COMPANY_HTML}</a>
  </div>
</section>
</body>
</html>
"""


@app.get("/terms", response_class=HTMLResponse)
def terms():
    return legal_page(
        "Términos y Condiciones",
        f"""
        <p><strong>Última actualización:</strong> 22 de mayo de 2026</p>
        <p>
          Bienvenido a <strong>{PRODUCT_HTML}</strong>, producto oficial de <strong>{COMPANY_HTML}</strong>.
          {PRODUCT_HTML} es una aplicación de inteligencia artificial creada para asistencia en chat,
          generación de imágenes, productividad, programación, automatización, análisis de información,
          apoyo tecnológico y acceso a API Keys para desarrolladores o empresas.
        </p>

        <h3>1. Uso de la aplicación</h3>
        <p>El usuario acepta usar {PRODUCT_HTML} de forma legal, responsable y respetuosa.</p>

        <h3>2. Planes, API Keys y pagos</h3>
        <p>
          {PRODUCT_HTML} puede ofrecer planes gratuitos, planes premium y planes de API Key.
          Los pagos dentro de la aplicación se procesan mediante <strong>Google Play Billing</strong>.
        </p>

        <h3>3. Uso de APIs</h3>
        <p>
          Las API Keys son personales o empresariales según el plan adquirido.
          El usuario debe proteger su API Key y no compartirla públicamente.
          {COMPANY_HTML} puede limitar, suspender o revocar API Keys ante abuso, fraude,
          uso malicioso, sobrecarga del sistema o incumplimiento de estos términos.
        </p>

        <h3>4. Contacto</h3>
        <p><strong>Producto:</strong> {PRODUCT_HTML}</p>
        <p><strong>Empresa:</strong> {COMPANY_HTML}</p>
        <p><strong>Fundador CEO:</strong> {FOUNDER}</p>
        <p><strong>Correo oficial:</strong> {MAIN_EMAIL}</p>
        <p><strong>WhatsApp:</strong> +51 905 917 699</p>
        """
    )


@app.get("/privacy", response_class=HTMLResponse)
def privacy():
    return legal_page(
        "Política de Privacidad",
        f"""
        <p><strong>Última actualización:</strong> 22 de mayo de 2026</p>
        <p>
          Esta Política de Privacidad explica cómo {PRODUCT_HTML} recopila, usa, almacena y protege
          la información de usuarios, desarrolladores y empresas.
        </p>

        <h3>1. Información que recopilamos</h3>
        <ul>
          <li>Correo electrónico del usuario.</li>
          <li>Plan activo del usuario.</li>
          <li>Historial de mensajes enviados a la IA.</li>
          <li>Respuestas generadas por la IA.</li>
          <li>Historial de imágenes generadas.</li>
          <li>Proyectos creados por el usuario.</li>
          <li>Información de suscripción o compra procesada por Google Play Billing.</li>
          <li>Información de API Key, plan developer o acceso empresarial.</li>
        </ul>

        <h3>2. Pagos y Google Play Billing</h3>
        <p>
          Los pagos dentro de {PRODUCT_HTML} se procesan mediante Google Play Billing.
          {PRODUCT_HTML} no almacena números de tarjetas, CVV, claves bancarias ni datos completos de pago.
        </p>

        <h3>3. API Keys</h3>
        <p>
          Cuando un usuario compra un plan API Key, {PRODUCT_HTML} puede almacenar datos necesarios
          para activar, validar y administrar esa API Key.
        </p>

        <h3>4. Contacto</h3>
        <p><strong>Correo:</strong> {MAIN_EMAIL}</p>
        <p><strong>WhatsApp:</strong> +51 905 917 699</p>
        """
    )


@app.get("/support", response_class=HTMLResponse)
def support():
    return legal_page(
        "Soporte Oficial",
        f"""
        <p>
          Para soporte técnico, privacidad, eliminación de datos, consultas de cuenta,
          información de planes, API Keys o ayuda con {PRODUCT_HTML}, contacta al equipo oficial.
        </p>

        <p><strong>WhatsApp:</strong> +51 905 917 699</p>
        <p><strong>Correo:</strong> {MAIN_EMAIL}</p>
        <p><strong>Producto:</strong> {PRODUCT_HTML}</p>
        <p><strong>Empresa:</strong> {COMPANY_HTML}</p>
        <p><strong>Fundador CEO:</strong> {FOUNDER}</p>

        <p>
          <a class="btn green" href="{WHATSAPP_LINK}" target="_blank">Abrir soporte por WhatsApp</a>
        </p>
        """
    )


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots_txt():
    return f"""User-agent: *
Allow: /

Disallow: /admin
Disallow: /admin/
Disallow: /admin/login
Disallow: /admin/api-keys
Disallow: /api/key/admin/todas

Sitemap: {SITE_URL}/sitemap.xml
"""


@app.get("/sitemap.xml", response_class=PlainTextResponse)
def sitemap_xml():
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}/</loc>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{SITE_URL}/terms</loc>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>{SITE_URL}/privacy</loc>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>{SITE_URL}/support</loc>
    <priority>0.6</priority>
  </url>
</urlset>
"""


@app.get("/health")
def health():
    return {
        "status": "online",
        "project": "AMERICO AI WEB PRO ADMIN",
        "product": "CENTENO AI",
        "app_link": APP_LINK,
        "google_verification": "active",
        "api_key_access": "inside_centeno_ai_with_google_play_billing",
        "api_key_generator": "active",
        "api_base_url": API_BASE_URL,
        "admin_panel": "/admin/login",
        "admin_api_keys_panel": "/admin/api-keys",
        "my_keys_endpoint": "/api/key/mis-keys?email=correo@gmail.com",
        "activate_key_endpoint": "/api/key/activar"
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
