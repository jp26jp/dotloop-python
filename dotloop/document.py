import logging
from typing import Optional

from .bases import DotloopObject

logger = logging.getLogger(__name__)

class Document(DotloopObject):
    """Represents a document in the Dotloop API."""

    ID_FIELD = 'document_id'

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a Document object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        logger.debug(f"Document initialized with parent: {parent}")

    def __call__(self, document_id: str) -> 'Document':
        """
        Set the document ID for this Document instance.

        Args:
            document_id (str): The ID of the document.

        Returns:
            Document: A new Document instance with the specified document_id.
        """
        logger.debug(f"Document.__call__() called with document_id: {document_id}")
        return super().__call__(document_id)

    def get(self) -> dict[str, any]:
        """
        Retrieve document information.

        If document_id is set, retrieves a specific document.
        If document_id is not set, retrieves all documents in the folder.

        Returns:
            dict[str, any]: The document information.

        Raises:
            DotloopAPIException: If there's an error retrieving the document information.
        """
        logger.debug(f"Document.get() called with id_value: {self.id_value}")
        return self.fetch('get')

    def post(self, **kwargs: any) -> dict[str, any]:
        """
        Create a new document.

        Args:
            **kwargs: The document fields for the new document.

        Returns:
            dict[str, any]: The newly created document information.

        Raises:
            DotloopAPIException: If there's an error creating the document.
        """
        logger.debug(f"Document.post() called with kwargs: {kwargs}")
        return self.fetch('post', json=kwargs)
