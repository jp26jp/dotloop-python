import requests

from .bases import DotloopObject
from .exceptions import DotloopAPIException


class Account(DotloopObject):
    """
    Represents a Dotloop account.

    This class provides methods to interact with account-related endpoints.
    """

    def get(self) -> dict:
        """
        Retrieve account details.

        Returns:
            dict: A dictionary containing account information.

        Raises:
            DotloopAPIException: If there's an error retrieving the account details.
        """

        try:
            return self.fetch("get")
        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if e.response is not None else None
            raise DotloopAPIException(f"Error retrieving account details: {str(e)}", status_code=status_code) from e
        except Exception as e:
            raise DotloopAPIException(f"Unexpected error retrieving account details: {str(e)}") from e
