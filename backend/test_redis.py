
import asyncio
import uuid

from src.db.redis import (
    add_jti_to_blocklist,
    token_in_blocklist,
    token_blocklist,
)


async def main():
    test_jti = f"test-{uuid.uuid4()}"

    try:
        # Before revocation, the JTI should not be blocked.
        result_before = await token_in_blocklist(test_jti)
        print("Before revocation:", result_before)

        # Add the JTI to Redis.
        await add_jti_to_blocklist(test_jti)

        # After revocation, the JTI should be blocked.
        result_after = await token_in_blocklist(test_jti)
        print("After revocation:", result_after)

        # Verify the key has an expiry.
        ttl = await token_blocklist.ttl(test_jti)
        print("Remaining TTL:", ttl)

    finally:
        # Remove only this test key.
        await token_blocklist.delete(test_jti)
        await token_blocklist.aclose()


asyncio.run(main())
