import logging
from typing import Optional

from .bases import DotloopObject

logger = logging.getLogger(__name__)

class LoopIt(DotloopObject):
    """Represents a LoopIt operation in the Dotloop API."""

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a LoopIt object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        self.profile_id: Optional[str] = None

    def post(self, **kwargs: any) -> dict[str, any]:
        """
        Create a new loop using the LoopIt functionality.

        Args:
            **kwargs: The fields for creating the new loop.

        Returns:
            dict[str, any]: The newly created loop information.

        Raises:
            DotloopAPIException: If there's an error creating the loop.
        """
        if self.profile_id is None:
            raise ValueError("profile_id must be set before calling post()")

        return self.fetch('post', json=kwargs, params={'profile_id': self.profile_id})
