import logging
from typing import Optional

from .bases import DotloopObject

logger = logging.getLogger(__name__)


class Participant(DotloopObject):
    """Represents a participant in a Dotloop loop."""

    ID_FIELD = 'participant_id'

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a Participant object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        self.participant_id: Optional[str] = None

    def __call__(self, participant_id: str) -> 'Participant':
        """
        Set the participant ID for this Participant instance.

        Args:
            participant_id (str): The ID of the participant.

        Returns:
            Participant: A new Participant instance with the specified participant_id.
        """
        logger.debug(f"Participant.__call__() called with participant_id: {participant_id}")
        return super().__call__(participant_id)

    def delete(self) -> dict[str, any]:
        """
        Delete the participant from the loop.

        Returns:
            dict[str, any]: The response from the server.

        Raises:
            DotloopAPIException: If there's an error deleting the participant.
        """
        logger.debug(f"Participant.delete() called with id_value: {self.id_value}")
        return self.fetch('delete')

    def get(self) -> dict[str, any]:
        """
        Retrieve participant information.

        If participant_id is set, retrieves a specific participant.
        If participant_id is not set, retrieves all participants in the loop.

        Returns:
            dict[str, any]: The participant information.

        Raises:
            DotloopAPIException: If there's an error retrieving the participant information.
        """
        logger.debug(f"Participant.get() called with id_value: {self.id_value}")
        return self.fetch('get')

    def patch(self, **kwargs: any) -> dict[str, any]:
        """
        Update the participant information.

        Args:
            **kwargs: The participant fields to update.

        Returns:
            dict[str, any]: The updated participant information.

        Raises:
            DotloopAPIException: If there's an error updating the participant information.
        """
        logger.debug(f"Participant.patch() called with kwargs: {kwargs}")
        return self.fetch('patch', json=kwargs)

    def post(self, **kwargs: any) -> dict[str, any]:
        """
        Create a new participant in the loop.

        Args:
            **kwargs: The participant fields for the new participant.

        Returns:
            dict[str, any]: The newly created participant information.

        Raises:
            DotloopAPIException: If there's an error creating the participant.
        """
        logger.debug(f"Participant.post() called with kwargs: {kwargs}")
        return self.fetch('post', json=kwargs)
