from base64 import b64encode
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
            base_url=CONST.LLM_API_URL,
        )
        self.model = CONST.LLM_MODEL
        self.max_tokens = CONST.LLM_MAX_TOKENS
        self.temperature = CONST.LLM_TEMPERATURE
        self.system_prompt = CONST.LLM_SYSTEM_PROMPT

    def _prepare_image_content(
        self,
        image_url: str | None = None,
        image_data: bytes | None = None,
        image_type: str | None = None,
    ) -> str:
        """
        Prepare image content as a string for the API request.

        Parameters
        ----------
        image_url : Optional[str]
            URL of the hosted image
        image_data : Optional[bytes]
            Raw image data
        image_type : Optional[str]
            MIME type of the image if using raw data

        Returns
        -------
        str
            Formatted image content for the API
        """
        if image_url:
            return f"Image URL: {image_url}"
        if image_data and image_type:
            b64_image = b64encode(image_data).decode("utf-8")
            return f"Image Data: data:{image_type};base64,{b64_image}"

        msg = "Either image_url or both image_data and image_type must be provided"
        raise ValueError(msg)

    async def get_response(
        self,
        prompt: str,
        image_url: str | None = None,
        image_data: bytes | None = None,
        image_type: str | None = None,
    ) -> str:
        """
        Send a prompt to the LLM and retrieve the complete response.

        Parameters
        ----------
        prompt : str
            The input text prompt for the LLM.
        image_url : Optional[str]
            URL of an image to analyze
        image_data : Optional[bytes]
            Raw image data to analyze
        image_type : Optional[str]
            MIME type of the image if using raw data

        Returns
        -------
        str
            The complete AI-generated response.
        """
        content: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        if image_url or image_data:
            image_content = self._prepare_image_content(image_url, image_data, image_type)
            content.append({"role": "user", "content": image_content})  # Content is now a string

        messages: list[ChatCompletionMessageParam] = content

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

    async def get_streaming_response(
        self,
        prompt: str,
        image_url: str | None = None,
        image_data: bytes | None = None,
        image_type: str | None = None,
    ) -> AsyncGenerator[str, None]:
        """
        Send a prompt to the LLM and stream the response chunks.

        Parameters
        ----------
        prompt : str
            The input text prompt for the LLM.
        image_url : Optional[str]
            URL of an image to analyze
        image_data : Optional[bytes]
            Raw image data to analyze
        image_type : Optional[str]
            MIME type of the image if using raw data

        Yields
        -------
        str
            Chunks of the AI-generated response as they arrive.
        """
        content = [prompt]

        if image_url or image_data:
            image_content = self._prepare_image_content(image_url, image_data, image_type)
            content.append(image_content)

        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": "\n".join(content)},  # Combine prompt and image info
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
