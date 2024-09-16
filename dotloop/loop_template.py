import logging
from typing import Optional

from .bases import DotloopObject

logger = logging.getLogger(__name__)

class LoopTemplate(DotloopObject):
    """Represents a loop template in the Dotloop API."""

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a LoopTemplate object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        self.loop_template_id: Optional[str] = None

    def get(self) -> dict[str, any]:
        """
        Retrieve loop template information.

        Returns:
            dict[str, any]: The loop template information.

        Raises:
            DotloopAPIException: If there's an error retrieving the loop template information.
        """
        return self.fetch('get')
