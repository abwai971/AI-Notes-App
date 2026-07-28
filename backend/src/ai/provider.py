from google import genai
from google.genai import types

from src.config import Config


class GeminiProvider:
    """
    Wrapper around the Gemini API.

    Responsible only for sending prompts to Gemini and
    returning the generated text.
    """

    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model = Config.GEMINI_MODEL

    async def generate(self,prompt: str,*,temperature: float = 0.3,) -> str:
        """
        Send a prompt to Gemini and return the generated text.

        Args:
            prompt: The prompt to send to Gemini.
            temperature: Sampling temperature for generation.

        Returns:
            The generated response text.

        Raises:
            RuntimeError: If the Gemini API request fails or returns
                          an empty response.
        """
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                ),
            )

            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text.strip()

        except Exception as e:
            raise RuntimeError("Gemini API request failed.") from e


gemini_provider = GeminiProvider()