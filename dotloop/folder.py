import logging
from typing import Optional

from .bases import DotloopObject
from .document import Document

logger = logging.getLogger(__name__)

class Folder(DotloopObject):
    """Represents a folder in the Dotloop API."""

    ID_FIELD = 'folder_id'

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a Folder object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        logger.debug(f"Folder initialized with parent: {parent}")

    def __call__(self, folder_id: str) -> 'Folder':
        """
        Set the folder ID for this Folder instance.

        Args:
            folder_id (str): The ID of the folder.

        Returns:
            Folder: A new Folder instance with the specified folder_id.
        """
        logger.debug(f"Folder.__call__() called with folder_id: {folder_id}")
        return super().__call__(folder_id)

    @property
    def document(self) -> Document:
        """
        Get a Document object associated with this folder.

        Returns:
            Document: A Document object.
        """
        return Document(parent=self)

    def get(self) -> dict[str, any]:
        """
        Retrieve folder information.

        If folder_id is set, retrieves a specific folder.
        If folder_id is not set, retrieves all folders in the loop.

        Returns:
            dict[str, any]: The folder information.

        Raises:
            DotloopAPIException: If there's an error retrieving the folder information.
        """
        logger.debug(f"Folder.get() called with id_value: {self.id_value}")
        return self.fetch('get')

    def patch(self, **kwargs: any) -> dict[str, any]:
        """
        Update the folder information.

        Args:
            **kwargs: The folder fields to update.

        Returns:
            dict[str, any]: The updated folder information.

        Raises:
            DotloopAPIException: If there's an error updating the folder information.
        """
        logger.debug(f"Folder.patch() called with kwargs: {kwargs}")
        return self.fetch('patch', json=kwargs)

    def post(self, **kwargs: any) -> dict[str, any]:
        """
        Create a new folder.

        Args:
            **kwargs: The folder fields for the new folder.

        Returns:
            dict[str, any]: The newly created folder information.

        Raises:
            DotloopAPIException: If there's an error creating the folder.
        """
        return self.fetch('post', json=kwargs)
