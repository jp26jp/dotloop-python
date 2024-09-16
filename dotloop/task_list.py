import logging
from typing import Optional, Generator

from .bases import DotloopObject
from .task import Task

logger = logging.getLogger(__name__)


class TaskList(DotloopObject):
    """Represents a task list in a Dotloop loop."""
    ID_FIELD = 'task_list_id'

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a TaskList object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        logger.debug(f"TaskList initialized with parent: {parent}, id_value: {self._id_value}")

    def __call__(self, task_list_id: str) -> 'TaskList':
        logger.debug(f"TaskList.__call__() called with task_list_id: {task_list_id}")
        return super().__call__(task_list_id)

    @property
    def task(self) -> Task:
        """
        Get a Task object associated with this task list.

        Returns:
            Task: A Task object.
        """
        return Task(parent=self)

    def get(self) -> dict[str, any]:
        """
        Retrieve task list information.

        Returns:
            dict[str, any]: The task list information.
        """
        logger.debug(f"TaskList.get() called with id_value: {self.id_value}")
        return self.fetch('get')

    def get_all(self, batch_size: int = 100) -> Generator[dict[str, any], None, None]:
        """
        Retrieve all task lists for a loop, handling pagination.

        Args:
            batch_size (int): Number of task lists to retrieve per request. Max is 100.

        Yields:
            dict[str, any]: Task list information for each task list.
        """
        batch_number = 1
        total_task_lists = None
        task_lists_fetched = 0

        while total_task_lists is None or task_lists_fetched < total_task_lists:
            logger.debug(f"Fetching task lists batch {batch_number} with size {batch_size}")
            params = {
                'batch_number': batch_number,
                'batch_size': min(batch_size, 100)
            }
            response = self.fetch('get', params=params)

            if total_task_lists is None:
                total_task_lists = response.get('meta', {}).get('total')
                logger.debug(f"Total task lists to fetch: {total_task_lists}")

            task_lists = response.get('data', [])
            for task_list in task_lists:
                yield task_list
                task_lists_fetched += 1

            if len(task_lists) < batch_size:
                break

            batch_number += 1

        logger.debug(f"Finished fetching task lists. Total fetched: {task_lists_fetched}")
