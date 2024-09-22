import httpx


class InspiroBot:
    def __init__(self):
        self.base_url = "https://inspirobot.me/api?generate=true"

    async def get_image(self) -> str:
        """
        Get a random motivational image from Inspirobot.

        Returns
        -------
        str
            The URL of the image.
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.base_url)
            response.raise_for_status()
            return response.text
