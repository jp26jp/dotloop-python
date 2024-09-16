from typing import Optional

from .bases import DotloopObject
from .exceptions import DotloopAPIException


class Activity(DotloopObject):
    """
    Represents activities in a Dotloop loop.

    This class provides methods to interact with activity-related endpoints.
    """

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize an Activity object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        self.activity_id: Optional[int] = None

    def get(self, batch_size: int = 20, batch_number: int = 1, **kwargs) -> dict:
        """
        Retrieve activities for a loop.

        Args:
            batch_size (int): Number of activities to retrieve per page (default: 20, max: 100).
            batch_number (int): Page number to retrieve (default: 1).
            **kwargs: Additional query parameters.

        Returns:
            dict: A dictionary containing activity information.

        Raises:
            DotloopAPIException: If there's an error retrieving the activities.
        """
        try:
            params = {
                "batch_size": min(batch_size, 100),  # Ensure batch_size doesn't exceed 100
                "batch_number": batch_number,
                **kwargs
            }
            return self.fetch('get', params=params)
        except Exception as e:
            raise DotloopAPIException(f"Error retrieving activities: {str(e)}") from e
