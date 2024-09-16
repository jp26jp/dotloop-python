import logging
from typing import Optional

from .activity import Activity
from .bases import DotloopObject
from .detail import Detail
from .folder import Folder
from .participant import Participant
from .task_list import TaskList

logger = logging.getLogger(__name__)


class Loop(DotloopObject):
    """Represents a loop in the Dotloop API."""
    ID_FIELD = "loop_id"

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a Loop object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        logger.debug(f"Loop initialized with parent: {parent}")

    def __call__(self, loop_id: str) -> 'Loop':
        """
        Allow setting the loop_id using method chaining.

        Args:
            loop_id (str): The ID of the loop to retrieve.

        Returns:
            Loop: A new Loop instance with the specified loop_id.
        """
        logger.debug(f"Loop.__call__() called with loop_id: {loop_id}")
        return super().__call__(loop_id)

    @property
    def activity(self) -> Activity:
        """
        Get an Activity object associated with this loop.

        Returns:
            Activity: An Activity object.
        """
        return Activity(parent=self)

    @property
    def detail(self) -> Detail:
        """
        Get a Detail object associated with this loop.

        Returns:
            Detail: A Detail object.
        """
        return Detail(parent=self)

    @property
    def folder(self) -> Folder:
        """
        Get a Folder object associated with this loop.

        Returns:
            Folder: A Folder object.
        """
        return Folder(parent=self)

    @property
    def participant(self) -> Participant:
        """
        Get a Participant object associated with this loop.

        Returns:
            Participant: A Participant object.
        """
        return Participant(parent=self)

    @property
    def task_list(self) -> TaskList:
        """
        Get a TaskList object associated with this loop.

        Returns:
            TaskList: A TaskList object.
        """
        return TaskList(parent=self)

    def get(self, **kwargs: any) -> dict[str, any]:
        """
        Retrieve loop information.

        Args:
            **kwargs: Additional query parameters for the API request.

        Returns:
            dict[str, any]: The loop information.

        Raises:
            DotloopAPIException: If there's an error retrieving the loop information.
        """
        logger.debug(f"Loop.get() called with id_value: {self.id_value}")
        return self.fetch("get", params=kwargs)

    def post(self, **kwargs: any) -> dict[str, any]:
        """
        Create a new loop.

        Args:
            **kwargs: The loop fields for the new loop.

        Returns:
            dict[str, any]: The newly created loop information.

        Raises:
            DotloopAPIException: If there's an error creating the loop.
        """
        return self.fetch("post", json=kwargs)

    def patch(self, **kwargs: any) -> dict[str, any]:
        """
        Update the loop information.

        Args:
            **kwargs: The loop fields to update.

        Returns:
            dict[str, any]: The updated loop information.

        Raises:
            DotloopAPIException: If there's an error updating the loop information.
        """
        return self.fetch("patch", json=kwargs)
