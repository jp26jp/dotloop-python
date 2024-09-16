import logging
from typing import Optional, Generator

from .bases import DotloopObject

logger = logging.getLogger(__name__)

class Task(DotloopObject):
    """Represents a task in a Dotloop loop."""
    ID_FIELD = 'task_id'

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a Task object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        logger.debug(f"Task initialized with parent: {parent}, id_value: {self._id_value}")

    def __call__(self, task_id: str) -> 'Task':
        logger.debug(f"Task.__call__() called with task_id: {task_id}")
        return super().__call__(task_id)

    def get(self) -> dict[str, any]:
        """
        Retrieve task information.

        Returns:
            dict[str, any]: The task information.
        """
        logger.debug(f"Task.get() called with id_value: {self.id_value}")
        return self.fetch('get')

    def get_all(self, batch_size: int = 100) -> Generator[dict[str, any], None, None]:
        """
        Retrieve all tasks for a task list, handling pagination.

        Args:
            batch_size (int): Number of tasks to retrieve per request. Max is 100.

        Yields:
            dict[str, any]: Task information for each task.
        """
        batch_number = 1
        total_tasks = None
        tasks_fetched = 0

        while total_tasks is None or tasks_fetched < total_tasks:
            logger.debug(f"Fetching tasks batch {batch_number} with size {batch_size}")
            params = {
                'batch_number': batch_number,
                'batch_size': min(batch_size, 100)
            }
            response = self.fetch('get', params=params)

            if total_tasks is None:
                total_tasks = response.get('meta', {}).get('total')
                logger.debug(f"Total tasks to fetch: {total_tasks}")

            tasks = response.get('data', [])
            for task in tasks:
                yield task
                tasks_fetched += 1

            if len(tasks) < batch_size:
                break

            batch_number += 1

        logger.debug(f"Finished fetching tasks. Total fetched: {tasks_fetched}")
