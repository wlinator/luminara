import time
from typing import Any

import requests

from lib.const import CONST


class TwitchAPIError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"Twitch API Error {status_code}: {message}")


class TwitchClient:
    def __init__(self) -> None:
        self.client_id = CONST.TWITCH_CLIENT_ID
        self.client_secret = CONST.TWITCH_CLIENT_SECRET
        self.access_token: str | None = None
        self.token_expiry: float = 0.0
        self.base_url = "https://api.twitch.tv/helix"

    def get_app_access_token(self) -> None:
        """
        Obtain a new app access token from Twitch.
        """
        url = "https://id.twitch.tv/oauth2/token"
        params = {"client_id": self.client_id, "client_secret": self.client_secret, "grant_type": "client_credentials"}
        response = requests.post(url, params=params)
        if response.status_code != 200:
            raise TwitchAPIError(response.status_code, response.text)

        data = response.json()
        self.access_token = data["access_token"]
        self.token_expiry = time.time() + data.get("expires_in", 3600)

    def ensure_token(self) -> None:
        """
        Ensure that the access token is valid. Refresh if expired.
        """
        if not self.access_token or time.time() >= self.token_expiry:
            self.get_app_access_token()

    def get_headers(self) -> dict[str, str]:
        """
        Generate headers for Twitch API requests.
        """
        self.ensure_token()
        return {
            "Client-ID": self.client_id or "",
            "Authorization": f"Bearer {self.access_token}" if self.access_token else "",
        }

    def get_user_ids(self, login_names: list[str]) -> dict[str, str]:
        """
        Retrieve user IDs for given login names.

        Parameters
        ----------
        login_names : List[str]
            List of Twitch login names.

        Returns
        -------
        Dict[str, str]
            Mapping from login name to user ID.
        """
        url = f"{self.base_url}/users"
        headers = self.get_headers()
        params = [("login", name) for name in login_names]
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise TwitchAPIError(response.status_code, response.text)

        data = response.json().get("data", [])
        return {user["login"]: user["id"] for user in data}

    def get_streams(self, user_ids: list[str]) -> dict[str, Any]:
        """
        Retrieve stream information for given user IDs.

        Parameters
        ----------
        user_ids : List[str]
            List of Twitch user IDs.

        Returns
        -------
        Dict[str, Any]
            Mapping from user login name to stream data.
        """
        url = f"{self.base_url}/streams"
        headers = self.get_headers()
        params = [("user_id", uid) for uid in user_ids]
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise TwitchAPIError(response.status_code, response.text)

        streams = response.json().get("data", [])
        return {stream["user_login"]: stream for stream in streams}

    def check_account_exists(self, username: str) -> bool:
        """
        Check if a Twitch account exists for the specified username.

        Parameters
        ----------
        username : str
            The Twitch username to check.

        Returns
        -------
        bool
            True if the account exists, False otherwise.
        """
        url = f"{self.base_url}/users"
        headers = self.get_headers()
        params = {"login": username}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise TwitchAPIError(response.status_code, response.text)

        data = response.json().get("data", [])
        return len(data) > 0
