
import asyncio
from src.ai.provider import gemini_provider


async def main():
    text = "A note about improving an application's user interface."
    embedding = await gemini_provider.embed(text)

    print("Embedding dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])
    print(
        "Vector magnitude:",
        sum(value * value for value in embedding) ** 0.5,
    )


if __name__ == "__main__":
    asyncio.run(main())
