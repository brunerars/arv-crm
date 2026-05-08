#!/bin/bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d '{"email":"bruno@arv.com","password":"test123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
AUTH="Authorization: Bearer $TOKEN"

call() {
  local method=$1 url=$2 data=$3 label=$4
  if [ -n "$data" ]; then
    RESP=$(curl -s -w "\n%{http_code}" -X "$method" "$url" -H "$AUTH" -H "Content-Type: application/json" -d "$data")
  else
    RESP=$(curl -s -w "\n%{http_code}" -X "$method" "$url" -H "$AUTH")
  fi
  HTTP=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')
  SUMMARY=$(echo "$BODY" | python3 -c "
import sys,json
raw=sys.stdin.read().strip()
try:
    d=json.loads(raw)
    if isinstance(d,list): print(f'Array with {len(d)} items')
    elif isinstance(d,dict):
        if 'detail' in d: print(f'ERROR: {str(d[\"detail\"])[:250]}')
        else: print(f'Keys: {list(d.keys())[:10]}')
    else: print(str(d)[:250])
except: print(raw[:250])
" 2>&1)
  echo "$label | HTTP $HTTP | $SUMMARY"
  # Return body for extraction
  echo "$BODY" > /tmp/last_resp.json
}

echo "========================================="
echo "1. AUTH ENDPOINTS"
echo "========================================="

# Register (may already exist)
echo "--- Register new user ---"
RESP=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8000/api/auth/register -H "Content-Type: application/json" -d '{"email":"testapi2@arv.com","password":"test123","name":"API Tester 2","admin_secret":"arv-admin-setup-2024"}')
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
echo "POST /api/auth/register | HTTP $HTTP | $(echo $BODY | head -c 300)"

echo ""
call GET http://localhost:8000/api/auth/me "" "GET /api/auth/me"

echo ""
echo "--- Logout ---"
call POST http://localhost:8000/api/auth/logout "" "POST /api/auth/logout"

# Re-login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d '{"email":"bruno@arv.com","password":"test123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
AUTH="Authorization: Bearer $TOKEN"

echo ""
echo "========================================="
echo "2. EMPRESAS ENDPOINTS"
echo "========================================="

echo ""
call POST http://localhost:8000/api/empresas '{"razao_social":"Test Corp LTDA","nome_fantasia":"TestCorp","cnpj":"11222333000181","segmento":"Tecnologia","porte":"Pequena","cidade":"Sao Paulo","estado":"SP"}' "POST /api/empresas"
EMPRESA_ID=$(python3 -c "import json; print(json.load(open('/tmp/last_resp.json')).get('id','NONE'))" 2>/dev/null || echo "NONE")
echo "  -> empresa_id=$EMPRESA_ID"

echo ""
call GET http://localhost:8000/api/empresas "" "GET /api/empresas"

echo ""
call GET "http://localhost:8000/api/empresas/$EMPRESA_ID" "" "GET /api/empresas/{id}"

echo ""
call PUT "http://localhost:8000/api/empresas/$EMPRESA_ID" '{"nome_fantasia":"TestCorp Updated"}' "PUT /api/empresas/{id}"

echo ""
call POST "http://localhost:8000/api/empresas/$EMPRESA_ID/enrich-cnpj" "" "POST /api/empresas/{id}/enrich-cnpj"

echo ""
echo "========================================="
echo "3. CONTATOS ENDPOINTS"
echo "========================================="

echo ""
call POST http://localhost:8000/api/contatos "{\"nome\":\"Joao Silva\",\"email\":\"joao@test.com\",\"telefone\":\"11999999999\",\"cargo\":\"CTO\",\"empresa_id\":\"$EMPRESA_ID\"}" "POST /api/contatos"
CONTATO_ID=$(python3 -c "import json; print(json.load(open('/tmp/last_resp.json')).get('id','NONE'))" 2>/dev/null || echo "NONE")
echo "  -> contato_id=$CONTATO_ID"

echo ""
call GET http://localhost:8000/api/contatos "" "GET /api/contatos"

echo ""
call GET "http://localhost:8000/api/contatos/$CONTATO_ID" "" "GET /api/contatos/{id}"

echo ""
call PUT "http://localhost:8000/api/contatos/$CONTATO_ID" '{"cargo":"CEO"}' "PUT /api/contatos/{id}"

echo ""
echo "========================================="
echo "4. ORIGENS ENDPOINTS"
echo "========================================="

echo ""
call GET http://localhost:8000/api/origens "" "GET /api/origens"

echo ""
echo "========================================="
echo "5. LEADS ENDPOINTS"
echo "========================================="

echo ""
call POST http://localhost:8000/api/leads "{\"empresa_id\":\"$EMPRESA_ID\",\"titulo\":\"Oportunidade TestCorp\",\"valor_estimado\":50000,\"origem\":\"indicacao\"}" "POST /api/leads"
LEAD_ID=$(python3 -c "import json; print(json.load(open('/tmp/last_resp.json')).get('id','NONE'))" 2>/dev/null || echo "NONE")
echo "  -> lead_id=$LEAD_ID"

echo ""
call GET http://localhost:8000/api/leads "" "GET /api/leads"

echo ""
call GET http://localhost:8000/api/leads/kanban "" "GET /api/leads/kanban"

echo ""
call GET "http://localhost:8000/api/leads/$LEAD_ID" "" "GET /api/leads/{id}"

echo ""
call PUT "http://localhost:8000/api/leads/$LEAD_ID" '{"valor_estimado":75000}' "PUT /api/leads/{id}"

echo ""
call POST "http://localhost:8000/api/leads/$LEAD_ID/change-stage" '{"new_stage":"contato_inicial"}' "POST /api/leads/{id}/change-stage"

echo ""
call GET "http://localhost:8000/api/leads/$LEAD_ID/completude" "" "GET /api/leads/{id}/completude"

echo ""
call GET "http://localhost:8000/api/leads/$LEAD_ID/historico" "" "GET /api/leads/{id}/historico"

echo ""
call POST "http://localhost:8000/api/leads/$LEAD_ID/calculate-score" "" "POST /api/leads/{id}/calculate-score"

echo ""
echo "========================================="
echo "6. ATIVIDADES ENDPOINTS"
echo "========================================="

echo ""
call POST http://localhost:8000/api/atividades "{\"lead_id\":\"$LEAD_ID\",\"tipo\":\"ligacao\",\"titulo\":\"Ligar para cliente\",\"descricao\":\"Follow up call\",\"data_prevista\":\"2026-03-25T10:00:00\"}" "POST /api/atividades"
ATIVIDADE_ID=$(python3 -c "import json; print(json.load(open('/tmp/last_resp.json')).get('id','NONE'))" 2>/dev/null || echo "NONE")
echo "  -> atividade_id=$ATIVIDADE_ID"

echo ""
call GET http://localhost:8000/api/atividades "" "GET /api/atividades"

echo ""
call POST "http://localhost:8000/api/atividades/$ATIVIDADE_ID/complete" "" "POST /api/atividades/{id}/complete"

echo ""
echo "========================================="
echo "7. DASHBOARD ENDPOINT"
echo "========================================="

echo ""
call GET http://localhost:8000/api/dashboard "" "GET /api/dashboard"

echo ""
echo "========================================="
echo "DONE"
echo "========================================="
