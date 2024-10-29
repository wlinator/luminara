from collections.abc import AsyncGenerator

from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
)

from lib.const import CONST


class OpenAIWrapper:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=CONST.LLM_API_KEY,
        )
        self.model = CONST.LLM_MODEL
        self.max_tokens = CONST.LLM_MAX_TOKENS
        self.temperature = CONST.LLM_TEMPERATURE
        self.system_prompt = CONST.LLM_SYSTEM_PROMPT

    async def get_response(self, prompt: str) -> str:
        """
        Send a prompt to the LLM and retrieve the complete response.

        Parameters
        ----------
        prompt : str
            The input text prompt for the LLM.

        Returns
        -------
        str
            The complete AI-generated response.
        """
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        response: ChatCompletion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return (
            response.choices[0].message.content.strip()
            if response.choices[0].message.content
            else "No response was generated."
        )

    async def get_streaming_response(self, prompt: str) -> AsyncGenerator[str, None]:
        """
        Send a prompt to the LLM and stream the response chunks.

        Parameters
        ----------
        prompt : str
            The input text prompt for the LLM.

        Yields
        -------
        str
            Chunks of the AI-generated response as they arrive.
        """
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=True,
        )

        async for chunk in stream:
            if content := chunk.choices[0].delta.content:
                yield content
