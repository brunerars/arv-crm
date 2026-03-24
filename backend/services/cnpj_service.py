import json
import httpx
import redis.asyncio as aioredis
from config import settings

CACHE_TTL = 60 * 60 * 24  # 24h

_redis = None
_http_client = None

def _get_redis():
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis

def _get_http_client():
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(timeout=10)
    return _http_client


async def enrich_empresa_cnpj(empresa, db):
    cnpj_clean = empresa.cnpj.replace(".", "").replace("/", "").replace("-", "")

    cache_key = f"cnpj:{cnpj_clean}"
    cached = await _get_redis().get(cache_key)

    if cached:
        data = json.loads(cached)
    else:
        resp = await _get_http_client().get(f"https://receitaws.com.br/v1/cnpj/{cnpj_clean}")
        if resp.status_code != 200:
            return empresa
        data = resp.json()
        if data.get("status") == "ERROR":
            return empresa
        await _get_redis().set(cache_key, json.dumps(data), ex=CACHE_TTL)

    if data.get("fantasia"):
        empresa.nome_fantasia = data["fantasia"]
    if data.get("nome"):
        empresa.razao_social = data["nome"]
    if data.get("municipio"):
        empresa.cidade = data["municipio"]
    if data.get("uf"):
        empresa.estado = data["uf"]
    if data.get("cep"):
        empresa.cep = data["cep"].replace(".", "")
    if data.get("telefone"):
        empresa.telefone = data["telefone"]

    await db.commit()
    await db.refresh(empresa)
    return empresa
