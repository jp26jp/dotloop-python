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
        except Exception as e:
            raise DotloopAPIException(f"Error retrieving account details: {str(e)}") from e
