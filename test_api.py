import urllib.request
import urllib.error
import json

BASE = "http://localhost:8000/api"

def req(method, path, data=None, headers=None):
    url = f"{BASE}{path}"
    body = json.dumps(data).encode() if data else None
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    r = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        resp = urllib.request.urlopen(r)
        raw = resp.read().decode()
        if not raw.strip():
            return resp.status, {"_empty": True}
        return resp.status, json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        if not raw.strip():
            return e.code, {"_empty": True, "_error": True}
        try:
            body = json.loads(raw)
        except:
            body = raw[:300]
        return e.code, body

def p(label, status, body):
    if isinstance(body, list):
        summary = f"Array with {len(body)} items"
    elif isinstance(body, dict):
        if "detail" in body:
            summary = f"ERROR: {str(body['detail'])[:300]}"
        else:
            summary = f"Keys: {list(body.keys())[:12]}"
    else:
        summary = str(body)[:300]
    ok = "OK" if status < 400 else "FAIL"
    print(f"  {ok} | HTTP {status} | {label}")
    print(f"       {summary}")
    return body

# 1. AUTH
print("=" * 60)
print("1. AUTH ENDPOINTS")
print("=" * 60)

s, b = req("POST", "/auth/register", {
    "email": "testapi4@arv.com", "password": "test123",
    "name": "API Tester 4", "admin_secret": "arv-admin-setup-2024"
})
p("POST /api/auth/register", s, b)

s, b = req("POST", "/auth/login", {
    "email": "bruno@arv.com", "password": "test123"
})
p("POST /api/auth/login", s, b)
TOKEN = b["access_token"]
H = {"Authorization": f"Bearer {TOKEN}"}

s, b = req("GET", "/auth/me", headers=H)
p("GET /api/auth/me", s, b)

s, b = req("POST", "/auth/logout", headers=H)
p("POST /api/auth/logout", s, b)

# Re-login
s, b = req("POST", "/auth/login", {
    "email": "bruno@arv.com", "password": "test123"
})
TOKEN = b["access_token"]
H = {"Authorization": f"Bearer {TOKEN}"}

# 2. EMPRESAS
print()
print("=" * 60)
print("2. EMPRESAS ENDPOINTS")
print("=" * 60)

s, b = req("POST", "/empresas", {
    "razao_social": "Test Corp LTDA", "nome_fantasia": "TestCorp",
    "cnpj": f"{hash('cnpj'+str(__import__('time').time())) % 10**14:014d}", "segmento": "Tecnologia",
    "porte": "Pequena", "cidade": "Sao Paulo", "estado": "SP"
}, H)
p("POST /api/empresas", s, b)
EMPRESA_ID = b.get("id", "NONE") if isinstance(b, dict) else "NONE"
print(f"       empresa_id={EMPRESA_ID}")

s, b = req("GET", "/empresas", headers=H)
p("GET /api/empresas", s, b)

s, b = req("GET", f"/empresas/{EMPRESA_ID}", headers=H)
p("GET /api/empresas/{{id}}", s, b)

s, b = req("PUT", f"/empresas/{EMPRESA_ID}", {"nome_fantasia": "TestCorp Updated"}, H)
p("PUT /api/empresas/{{id}}", s, b)

s, b = req("POST", f"/empresas/{EMPRESA_ID}/enrich-cnpj", headers=H)
p("POST /api/empresas/{{id}}/enrich-cnpj", s, b)

# 3. CONTATOS
print()
print("=" * 60)
print("3. CONTATOS ENDPOINTS")
print("=" * 60)

s, b = req("POST", "/contatos", {
    "nome": "Joao Silva", "email": "joao2@test.com",
    "telefone": "11999999999", "cargo": "CTO",
    "empresa_id": EMPRESA_ID
}, H)
p("POST /api/contatos", s, b)
CONTATO_ID = b.get("id", "NONE") if isinstance(b, dict) else "NONE"
print(f"       contato_id={CONTATO_ID}")

s, b = req("GET", "/contatos", headers=H)
p("GET /api/contatos", s, b)

s, b = req("GET", f"/contatos/{CONTATO_ID}", headers=H)
p("GET /api/contatos/{{id}}", s, b)

s, b = req("PUT", f"/contatos/{CONTATO_ID}", {"cargo": "CEO"}, H)
p("PUT /api/contatos/{{id}}", s, b)

# 4. ORIGENS
print()
print("=" * 60)
print("4. ORIGENS ENDPOINTS")
print("=" * 60)

s, b = req("GET", "/origens", headers=H)
p("GET /api/origens", s, b)

# 5. LEADS
print()
print("=" * 60)
print("5. LEADS ENDPOINTS")
print("=" * 60)

s, b = req("POST", "/leads", {
    "empresa_id": EMPRESA_ID,
    "titulo": "Oportunidade TestCorp",
    "valor_estimado": 50000,
    "origem": "indicacao"
}, H)
p("POST /api/leads", s, b)
LEAD_ID = b.get("id", "NONE") if isinstance(b, dict) else "NONE"
print(f"       lead_id={LEAD_ID}")

s, b = req("GET", "/leads", headers=H)
p("GET /api/leads", s, b)

s, b = req("GET", "/leads/kanban", headers=H)
p("GET /api/leads/kanban", s, b)

s, b = req("GET", f"/leads/{LEAD_ID}", headers=H)
p("GET /api/leads/{{id}}", s, b)

s, b = req("PUT", f"/leads/{LEAD_ID}", {"valor_estimado": 75000}, H)
p("PUT /api/leads/{{id}}", s, b)

s, b = req("POST", f"/leads/{LEAD_ID}/change-stage", {"nova_etapa": "primeiro_contato"}, H)
p("POST /api/leads/{{id}}/change-stage", s, b)

s, b = req("GET", f"/leads/{LEAD_ID}/completude", headers=H)
p("GET /api/leads/{{id}}/completude", s, b)

s, b = req("GET", f"/leads/{LEAD_ID}/historico", headers=H)
p("GET /api/leads/{{id}}/historico", s, b)

s, b = req("POST", f"/leads/{LEAD_ID}/calculate-score", headers=H)
p("POST /api/leads/{{id}}/calculate-score", s, b)

# 6. ATIVIDADES
print()
print("=" * 60)
print("6. ATIVIDADES ENDPOINTS")
print("=" * 60)

s, b = req("POST", "/atividades", {
    "lead_id": LEAD_ID,
    "tipo": "ligacao",
    "titulo": "Ligar para cliente",
    "descricao": "Follow up call",
    "data_prevista": "2026-03-25T10:00:00"
}, H)
p("POST /api/atividades", s, b)
ATIVIDADE_ID = b.get("id", "NONE") if isinstance(b, dict) else "NONE"
print(f"       atividade_id={ATIVIDADE_ID}")

s, b = req("GET", "/atividades", headers=H)
p("GET /api/atividades", s, b)

s, b = req("POST", f"/atividades/{ATIVIDADE_ID}/complete", headers=H)
p("POST /api/atividades/{{id}}/complete", s, b)

# 7. DASHBOARD
print()
print("=" * 60)
print("7. DASHBOARD ENDPOINT")
print("=" * 60)

s, b = req("GET", "/dashboard", headers=H)
p("GET /api/dashboard", s, b)

print()
print("=" * 60)
print("ALL TESTS COMPLETE")
print("=" * 60)
