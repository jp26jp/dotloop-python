import logging
import time
from functools import cached_property
from typing import Optional

import requests

from .account import Account
from .authenticate import Authenticate
from .contact import Contact
from .exceptions import DotloopAPIException, DotloopAuthException
from .profile import Profile
from .bases import endpoint_directory, DotloopObject

logger = logging.getLogger(__name__)

class Client(DotloopObject):
    """Client class for interacting with the Dotloop API."""
    endpoint_directory = endpoint_directory

    def __init__(self, access_token: str, client_id: str, client_secret: str, refresh_token: str):
        super().__init__()
        self._session = requests.Session()
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth = Authenticate(client_id, client_secret)
        self._update_session_headers()


    def __str__(self) -> str:
        """Return a string representation of the Client."""
        return "<Client>"


    @property
    def access_token(self) -> str:
        """Get the current access token."""
        return self._access_token

    @access_token.setter
    def access_token(self, value: str) -> None:
        """
        Set a new access token and update session headers.

        Args:
            value (str): The new access token.
        """
        self._access_token = value
        self._update_session_headers()

    def _update_session_headers(self) -> None:
        """Update the session headers with the current access token."""
        self._session.headers.update(self._headers)
        logger.debug(f"Debug: Headers set to {self._session.headers}")  # Add this line

    def is_token_valid(self) -> bool:
        """
        Check if the current access token is valid by making a lightweight API call.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            response = self.account.get()
            logger.debug(f"Token validation response: {response}")
            return True
        except DotloopAuthException:
            logger.info("Token is invalid (401 Unauthorized)")
            return False
        except DotloopAPIException as e:
            logger.error(f"Unexpected API exception during token validation: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in is_token_valid: {e}")
            return False

    def ensure_valid_token(self):
        """
        Ensure that the client has a valid token, refreshing if necessary.

        Returns:
            dict: The refresh response if a refresh was performed, None otherwise.

        Raises:
            DotloopAuthException: If unable to refresh the token.
        """
        if self.is_token_valid():
            logger.info("Token is still valid")
            return None
        logger.info("Token is invalid, refreshing...")
        return self.refresh_token()

    def refresh_token(self) -> dict:
        """
        Refresh the access token using the refresh token.

        Returns:
            dict: The full response from the token refresh API call.

        Raises:
            DotloopAuthException: If there's an error refreshing the token.
        """
        try:
            response = self._auth.refresh_access_token(self._refresh_token)

            if 'access_token' in response:
                self._access_token = response['access_token']
                self._update_session_headers()
            else:
                raise DotloopAuthException("No access token in refresh response")

            if 'refresh_token' in response:
                self._refresh_token = response['refresh_token']

            return response
        except Exception as e:
            raise DotloopAuthException(f"Error refreshing token: {str(e)}") from e

    @property
    def _headers(self) -> dict[str, str]:
        """Get the headers for API requests."""
        return {"Authorization": f"Bearer {self._access_token}"}

    @property
    def contact(self) -> Contact:
        """Get a Contact object."""
        return Contact(parent=self)

    @property
    def account(self) -> Account:
        """Get an Account object."""
        return Account(parent=self)

    @property
    def profile(self) -> Profile:
        """Get a Profile object."""
        return Profile(parent=self)


    @cached_property
    def default_profile(self) -> str:
        """
        Get the default profile ID.

        Returns:
            str: The default profile ID.

        Raises:
            DotloopAPIException: If unable to fetch the default profile ID.
        """
        try:
            profiles = self.profile.get()
            profile_data = profiles.get("data", [])

            # First, try to find a profile marked as default
            default_profile = next(
                (p["id"] for p in profile_data if p.get("default")), None
            )
            if default_profile:
                return default_profile

            # If no default profile is found, return the first profile ID
            if profile_data:
                return profile_data[0]["id"]

            raise DotloopAPIException("No profiles found")

        except Exception as e:
            if isinstance(e, DotloopAPIException):
                raise  # Re-raise DotloopAPIException if it's already that type
            error_message = str(e)
            raise DotloopAPIException(
                f"Unable to fetch default profile ID: {error_message}"
            ) from e

    def fetch(self, method: str, **kwargs) -> dict[str, any]:
        """
        Fetch data from the Dotloop API, ensuring a valid token before making the request.

        Args:
            method (str): The HTTP method to use.
            **kwargs: Additional keyword arguments for the request.

        Returns:
            dict[str, any]: The JSON response from the API.

        Raises:
            DotloopAPIException: If there's an error with the API request.
        """
        self.ensure_valid_token()

        try:
            response = getattr(self._session, method.lower())(**kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DotloopAPIException(f"API request failed: {str(e)}") from e
