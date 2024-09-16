from base64 import b64encode
from typing import Optional
from urllib.parse import urlencode, urljoin

import requests

from dotloop.exceptions import DotloopAuthException


class Authenticate:
    BASE_URL = "https://auth.dotloop.com/oauth/"
    GRANT_TYPE_AUTH_CODE = "authorization_code"
    GRANT_TYPE_REFRESH_TOKEN = "refresh_token"

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize the Authenticate object.

        Args:
            client_id (str): The client ID for authentication.
            client_secret (str): The client secret for authentication.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    @property
    def headers(self) -> dict[str, str]:
        """
        Get the headers for authentication requests.

        Returns:
            dict[str, str]: The headers dictionary.
        """
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}",
        }

    def url_for_authentication(
        self,
        redirect_uri: str,
        response_type: str = "code",
        state: Optional[str] = None,
        redirect_on_deny: bool = False,
    ) -> str:
        """
        Generate the URL for authentication.

        Args:
            redirect_uri (str): The URI to redirect to after authentication.
            response_type (str): The response type (default: 'code').
            state (Optional[str]): A random string to protect against CSRF.
            redirect_on_deny (bool): Whether to redirect on deny (default: False).

        Returns:
            str: The authentication URL.
        """
        endpoint = "authorize"
        params = {
            "response_type": response_type,
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "redirect_on_deny": redirect_on_deny,
        }
        if state is not None:
            params["state"] = state
        return f"{urljoin(self.BASE_URL, endpoint)}?{urlencode(params)}"

    def acquire_access_and_refresh_tokens(
        self, code: str, redirect_uri: str, state: Optional[str] = None
    ) -> dict:
        """
        Acquire access and refresh tokens using an authorization code.

        Args:
            code (str): The authorization code.
            redirect_uri (str): The redirect URI used in the initial request.
            state (Optional[str]): The state parameter used in the initial request.

        Returns:
            dict: A dictionary containing the access and refresh tokens.

        Raises:
            DotloopAuthException: If there's an error acquiring the tokens.
        """
        endpoint = "token"
        url = urljoin(self.BASE_URL, endpoint)
        try:
            response = self.session.post(
                url,
                params={
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "state": state,
                    "grant_type": self.GRANT_TYPE_AUTH_CODE,
                },
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DotloopAuthException(f"Error acquiring tokens: {str(e)}") from e

    def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Refresh the access token using a refresh token.

        Args:
            refresh_token (str): The refresh token.

        Returns:
            dict: A dictionary containing the new access token and refresh token.

        Raises:
            DotloopAuthException: If there's an error refreshing the token.
        """
        endpoint = "token"
        url = urljoin(self.BASE_URL, endpoint)
        try:
            response = self.session.post(
                url,
                params={
                    "grant_type": self.GRANT_TYPE_REFRESH_TOKEN,
                    "refresh_token": refresh_token,
                },
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DotloopAuthException(f"Error refreshing token: {str(e)}") from e

    def revoke_access(self, access_token: str) -> dict:
        """
        Revoke access for a given access token.

        Args:
            access_token (str): The access token to revoke.

        Returns:
            dict: The response from the server.

        Raises:
            DotloopAuthException: If there's an error revoking the token.
        """
        endpoint = "token/revoke"
        url = urljoin(self.BASE_URL, endpoint)
        try:
            response = self.session.post(url, params={"token": access_token})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DotloopAuthException(f"Error revoking token: {str(e)}") from e