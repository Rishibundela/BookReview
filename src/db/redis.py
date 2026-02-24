import redis.asyncio as aioredis
from src.config import Config

JTI_EXPIRY = 3600 # in seconds, adjust as needed (e.g., 1 hour)

token_blocklist = aioredis.from_url(Config.REDIS_URL)

async def add_token_to_blocklist(jti: str):
    await token_blocklist.set(name=jti, value="blocked", ex=JTI_EXPIRY)

async def is_token_blocked(jti: str):
    jti = await token_blocklist.get(jti)
    return jti is not None