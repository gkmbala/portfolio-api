from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re, smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

OWNER_EMAIL = "gkmbala@gmail.com"
SMTP_USER   = os.getenv("SMTP_USER", OWNER_EMAIL)
SMTP_PASS   = os.getenv("SMTP_PASS", "")

app = FastAPI(title="Balaji K. Portfolio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gkmbala.github.io",
        "http://localhost",
        "http://127.0.0.1",
        "null",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

CHAT_KB = {
    r"python|django|flask":
        "Balaji is highly proficient in Python — AI automation pipelines he built reduced operational overhead by 40%.",
    r"javascript|react|node|typescript":
        "Balaji works across the full JS stack — React on the frontend, Node.js on the backend.",
    r"php|laravel|magento|adobe|ecommerce":
        "Balaji is an Adobe Certified Magento Commerce Developer. He builds platforms processing 10,000+ daily transactions.",
    r"cloud|azure|aws|docker|kubernetes|devops":
        "Cloud & DevOps is a core strength — Azure, AWS, Docker, Kubernetes, Terraform and Ansible.",
    r"ci.?cd|jenkins|pipeline|deployment":
        "He built CI/CD pipelines from scratch improving deployment cycles by 50%.",
    r"ai|openai|automation|agentic|machine":
        "AI-driven automation is a key speciality — Python-based pipelines delivered 40% ops reduction at Lencarta.",
    r"power.?bi|zoho|analytics|data":
        "Balaji works with Power BI, Agentic Analytics BI, and Zoho Analytics for business intelligence.",
    r"lencarta|current.?job|current.?role":
        "Balaji is currently Technology Specialist at Lencarta Ltd in Leeds (Dec 2020–present).",
    r"experience|years|background":
        "Balaji has 14+ years of professional software development experience across India and the UK.",
    r"team|lead|manag|mentor":
        "Balaji leads teams of 5–8 developers and has mentored 10+ developers — 3 promoted to senior roles.",
    r"achiev|impact|result|win":
        "Key wins: 40% ops reduction, 50% faster deployments, 35% revenue increase, 15+ integrations, 99.9% uptime.",
    r"contact|email|hire|availab|reach":
        "Email Balaji at gkmbala@gmail.com or LinkedIn: linkedin.com/in/balaji-kaliyaperumal-41620192",
    r"skill|stack|tech|language":
        "Stack: Python, PHP, JavaScript, C#, Node.js, React, Adobe Commerce, Azure, Docker, Kubernetes, OpenAI, Power BI.",
    r"certif|adobe|ibm|microsoft":
        "Certifications: Adobe Certified Magento Commerce Developer, IBM AI Fundamentals, CSDA, Microsoft DevOps.",
    r"education|degree|university|mca":
        "Balaji holds an M.C.A. from Anna University and a B.Sc. in Electrical & Communications from AVC College.",
    r"location|leeds|uk|remote":
        "Based in Leeds, England, UK. Works with global distributed teams — remote and hybrid.",
    r"github|repo|project":
        "Balaji's GitHub is github.com/gkmbala — check it for live repositories and contributions.",
    r"salary|rate|pay":
        "For compensation discussions, contact Balaji directly at gkmbala@gmail.com.",
    r"hello|hi\b|hey\b":
        "Hi! I'm Balaji's portfolio assistant. Ask me anything about his skills, experience or how to get in touch! 👋",
    r"thank|thanks|cheers":
        "You're welcome! Feel free to ask anything else. 😊",
}

def chat_reply(msg: str, name: str = "") -> str:
    m = msg.lower()
    for pattern, reply in CHAT_KB.items():
        if re.search(pattern, m):
            return reply
    first = name.split()[0] if name else ""
    g = f"{first}, " if first else ""
    return f"Good question, {g}but I don't have a specific answer for that. Email Balaji at {OWNER_EMAIL} for more detail!"

def send_email(name: str, email: str, company: str = "") -> bool:
    if not SMTP_PASS:
        print("SMTP_PASS not set — skipping email")
        return False
    try:
        now = datetime.utcnow().strftime("%d %b %Y at %H:%M UTC")
        company_row = f"<tr><td style='color:#8b93b0;padding:0.4rem 0;'>Company</td><td style='padding:0.4rem 0;'>{company}</td></tr>" if company else ""
        html = f"""
<div style="font-family:Arial,sans-serif;max-width:500px;background:#0f1117;color:#e8ecf5;border-radius:12px;overflow:hidden;border:1px solid #2a3050;">
  <div style="background:linear-gradient(135deg,#6c8eff,#a78bfa);padding:1.2rem 1.6rem;">
    <h2 style="margin:0;color:#fff;font-size:1rem;">📬 New Portfolio Visitor</h2>
    <p style="margin:0.2rem 0 0;font-size:0.75rem;color:rgba(255,255,255,0.7);">{now}</p>
  </div>
  <div style="padding:1.2rem 1.6rem;">
    <table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
      <tr><td style="color:#8b93b0;padding:0.4rem 0;width:100px;">Name</td><td style="padding:0.4rem 0;font-weight:600;">{name}</td></tr>
      <tr><td style="color:#8b93b0;padding:0.4rem 0;">Email</td><td style="padding:0.4rem 0;"><a href="mailto:{email}" style="color:#6c8eff;">{email}</a></td></tr>
      {company_row}
      <tr><td style="color:#8b93b0;padding:0.4rem 0;">Source</td><td style="padding:0.4rem 0;">gkmbala.github.io</td></tr>
    </table>
    <div style="margin-top:1rem;padding:0.8rem;background:#1c2030;border-radius:8px;border:1px solid #2a3050;">
      <p style="margin:0;font-size:0.78rem;color:#8b93b0;">💡 <strong style="color:#e8ecf5;">Tip:</strong> Hit Reply to respond directly to {name}</p>
    </div>
  </div>
  <div style="padding:0.8rem 1.6rem;border-top:1px solid #2a3050;font-size:0.68rem;color:#505a7a;text-align:center;">
    Sent by your Render.com FastAPI backend
  </div>
</div>"""
        msg_obj = MIMEMultipart("alternative")
        msg_obj["Subject"]  = f"📬 Portfolio visitor: {name}"
        msg_obj["From"]     = SMTP_USER
        msg_obj["To"]       = OWNER_EMAIL
        msg_obj["Reply-To"] = email
        msg_obj.attach(MIMEText(html, "html"))
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.sendmail(SMTP_USER, OWNER_EMAIL, msg_obj.as_string())
        print(f"✅ Email sent for {name} <{email}>")
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

# ── Models ──────────────────────────────────────────
class ChatReq(BaseModel):
    message: str
    visitor_name: str = ""

class NotifyReq(BaseModel):
    name: str
    email: str
    company: str = ""

# ── Routes ──────────────────────────────────────────
@app.get("/")
def root():
    return {"api": "Balaji K. Portfolio API", "status": "ok",
            "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/profile")
def profile():
    return {"ok": True, "data": {
        "name": "Balaji Kaliyaperumal",
        "title": "Technology Specialist",
        "location": "Leeds, UK",
        "email": OWNER_EMAIL,
        "github": "https://github.com/gkmbala",
        "linkedin": "https://linkedin.com/in/balaji-kaliyaperumal-41620192",
        "experience_years": 14,
        "current_company": "Lencarta Ltd"
    }}
@app.get("/github")
def get_github():
    import httpx
    try:
        r = httpx.get(
            "https://api.github.com/users/gkmbala",
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=8.0
        )
        d = r.json()
        return {"ok": True, "data": {
            "login":        d.get("login"),
            "name":         d.get("name"),
            "avatar_url":   d.get("avatar_url"),
            "bio":          d.get("bio"),
            "public_repos": d.get("public_repos", 0),
            "followers":    d.get("followers", 0),
            "html_url":     d.get("html_url"),
        }}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/repos")
def get_repos(limit: int = 6):
    import httpx
    try:
        r = httpx.get(
            "https://api.github.com/users/gkmbala/repos",
            params={"sort": "updated", "per_page": 30, "type": "owner"},
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=8.0
        )
        repos = sorted(r.json(), key=lambda x: x.get("stargazers_count", 0), reverse=True)[:limit]
        return {"ok": True, "count": len(repos), "data": [
            {
                "name":        repo["name"],
                "description": repo.get("description"),
                "language":    repo.get("language"),
                "stars":       repo.get("stargazers_count", 0),
                "forks":       repo.get("forks_count", 0),
                "url":         repo["html_url"],
                "updated_at":  repo.get("updated_at")
            }
            for repo in repos
        ]}
    except Exception as e:
        return {"ok": False, "error": str(e)}
        
@app.post("/chat")
def chat(req: ChatReq):
    if len(req.message.strip()) < 2:
        raise HTTPException(status_code=400, detail="Message too short")
    return {
        "reply": chat_reply(req.message, req.visitor_name),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/notify")
def notify(req: NotifyReq):
    if not req.name or not req.email:
        raise HTTPException(status_code=400, detail="Name and email required")
    sent = send_email(req.name, req.email, req.company)
    return {"ok": True, "email_sent": sent,
            "timestamp": datetime.utcnow().isoformat()}
