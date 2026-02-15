import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600 # in seconds, adjust as needed (e.g., 1 hour)

token_blocklist = redis.Redis(
    host=Config.Redis_HOST,
    port=Config.Redis_PORT,
    decode_responses=True
)

async def add_token_to_blocklist(jti: str):
    await token_blocklist.set(name=jti, value="blocked", ex=JTI_EXPIRY)

async def is_token_blocked(jti: str):
    jti = await token_blocklist.get(jti)
    return jti is not None