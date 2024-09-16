from typing import Optional

from .bases import DotloopObject
import logging

logger = logging.getLogger(__name__)


class Detail(DotloopObject):
    """Represents details of a loop in the Dotloop API."""
    ID_FIELD = None

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a Detail object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)

    def get(self) -> dict[str, any]:
        """
        Retrieve the details of a loop.

        Returns:
            dict[str, any]: The loop details.

        Raises:
            DotloopAPIException: If there's an error retrieving the loop details.
        """
        return self.fetch('get')

    def patch(self, **kwargs: any) -> dict[str, any]:
        """
        Update the details of a loop.

        Args:
            **kwargs: The loop detail fields to update.

        Returns:
            dict[str, any]: The updated loop details.

        Raises:
            DotloopAPIException: If there's an error updating the loop details.
        """
        return self.fetch('patch', json=kwargs)
