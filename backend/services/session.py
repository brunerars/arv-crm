import redis.asyncio as redis
from config import settings

SESSION_TTL = 60 * 60 * 8  # 8 hours

_redis = None

def _get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


async def create_session(user_id: str, jti: str) -> None:
    key = f"session:{user_id}"
    await _get_redis().set(key, jti, ex=SESSION_TTL)


async def validate_session(user_id: str, jti: str) -> bool:
    key = f"session:{user_id}"
    stored_jti = await _get_redis().get(key)
    return stored_jti == jti


async def invalidate_session(user_id: str) -> None:
    key = f"session:{user_id}"
    await _get_redis().delete(key)
