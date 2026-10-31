
from redis import asyncio as aioredis

from src.config import Config


JTI_EXPIRY = 3600  # 1 hour, in seconds

token_blocklist = aioredis.from_url(
    Config.REDIS_URL,
    decode_responses=True,
)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="revoked",
        ex=JTI_EXPIRY,
    )


async def token_in_blocklist(jti: str) -> bool:
    result = await token_blocklist.get(jti)
    return result is not None


async def close_redis() -> None:
    await token_blocklist.aclose()
