from typing import Optional

from .bases import DotloopObject

import logging

logger = logging.getLogger(__name__)

class Contact(DotloopObject):
    """Represents a contact in the Dotloop API."""

    ID_FIELD = 'contact_id'

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a Contact object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        self.contact_id: Optional[str] = None


    def __call__(self, contact_id: str) -> 'Contact':
        logger.debug(f"Contact.__call__() called with contact_id: {contact_id}")
        return super().__call__(contact_id)


    def delete(self) -> dict[str, any]:
        """
        Delete the contact.

        Returns:
            dict[str, any]: The API response for the delete operation.

        Raises:
            DotloopAPIException: If there's an error deleting the contact.
        """
        logger.debug(f"Contact.delete() called with id_value: {self.id_value}")
        return self.fetch('delete')

    def get(self, **kwargs: any) -> dict[str, any]:
        """
        Retrieve contact information.

        Args:
            **kwargs: Additional query parameters for the API request.

        Returns:
            dict[str, any]: The contact information.

        Raises:
            DotloopAPIException: If there's an error retrieving the contact information.
        """
        logger.debug(f"Contact.get() called with id_value: {self.id_value}")
        return self.fetch('get')

    def patch(self, **kwargs: any) -> dict[str, any]:
        """
        Update the contact information.

        Args:
            **kwargs: The contact fields to update.

        Returns:
            dict[str, any]: The updated contact information.

        Raises:
            DotloopAPIException: If there's an error updating the contact information.
        """
        logger.debug(f"Contact.patch() called with kwargs: {kwargs}")
        return self.fetch('patch', json=kwargs)

    def post(self, **kwargs: any) -> dict[str, any]:
        """
        Create a new contact.

        Args:
            **kwargs: The contact fields for the new contact.

        Returns:
            dict[str, any]: The newly created contact information.

        Raises:
            DotloopAPIException: If there's an error creating the contact.
        """
        logger.debug(f"Contact.post() called with kwargs: {kwargs}")
        return self.fetch('post', json=kwargs)
