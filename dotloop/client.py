import logging
from functools import cached_property

import requests

from .account import Account
from .contact import Contact
from .exceptions import DotloopAPIException
from .profile import Profile
from .bases import endpoint_directory, DotloopObject

logger = logging.getLogger(__name__)

class Client(DotloopObject):
    """Client class for interacting with the Dotloop API."""
    endpoint_directory = endpoint_directory

    def __init__(self, access_token: str):
        """
        Initialize the Client.

        Args:
            access_token (str): The access token for API authentication.
        """
        super().__init__()
        self._session = requests.Session()
        self._access_token = access_token
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

    def fetch(self, method: str, endpoint: str, **kwargs: any) -> dict[str, any]:
        """
        Fetch data from the Dotloop API.

        Args:
            method (str): The HTTP method to use.
            endpoint (str): The API endpoint to call.
            **kwargs: Additional keyword arguments for the request.

        Returns:
            dict[str, any]: The JSON response from the API.

        Raises:
            DotloopAPIException: If there's an error with the API request.
        """
        try:
            response = getattr(self._session, method.lower())(endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise DotloopAPIException(f"API request failed: {str(e)}") from e
