import logging
from json import JSONDecodeError
from typing import Optional
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)


class NotNone:
    """A class to represent a value that is not None."""

    def __eq__(self, other: any) -> bool:
        """Check if the other value is not None."""
        return other is not None

    def __str__(self) -> str:
        """Return a string representation of NotNone."""
        return "NotNone"

    def __repr__(self) -> str:
        """Return a string representation of NotNone."""
        return str(self)


class EndpointDirectory:
    """A class to manage API endpoints."""

    def __init__(self):
        """Initialize the EndpointDirectory."""
        self._items = [
            # [(object, method, id_value), endpointToFormat]
            ("LoopIt", "post", None, "loop-it"),
            ("Account", "get", None, "account"),

            ("Profile", "get", None, "profile"),
            ("Profile", "get", NotNone, "profile/{profile_id}"),
            ("Profile", "post", None, "profile"),
            ("Profile", "patch", NotNone, "profile/{profile_id}"),

            ('Loop', 'get', None, 'profile/{profile_id}/loop'),
            ('Loop', 'get', NotNone, 'profile/{profile_id}/loop/{loop_id}'),
            ('Loop', 'post', None, 'profile/{profile_id}/loop'),
            ('Loop', 'patch', NotNone, 'profile/{profile_id}/loop/{loop_id}'),

            ("Detail", "get", None, "profile/{profile_id}/loop/{loop_id}/detail"),
            ("Detail", "patch", None, "profile/{profile_id}/loop/{loop_id}/detail"),

            ("Folder", "get", None, "profile/{profile_id}/loop/{loop_id}/folder"),
            ("Folder", "get", NotNone, "profile/{profile_id}/loop/{loop_id}/folder/{folder_id}"),
            ("Folder", "patch", NotNone, "profile/{profile_id}/loop/{loop_id}/folder/{folder_id}"),

            ("Document", "get", None, "profile/{profile_id}/loop/{loop_id}/folder/{folder_id}/document"),
            ("Document", "get", NotNone, "profile/{profile_id}/loop/{loop_id}/folder/{folder_id}/document/{document_id}"),
            ("Document", "post", None, "profile/{profile_id}/loop/{loop_id}/folder/{folder_id}/document"),

            ("Participant", "get", None, "profile/{profile_id}/loop/{loop_id}/participant"),
            ("Participant", "get", NotNone, "profile/{profile_id}/loop/{loop_id}/participant/{participant_id}"),
            (
                "Participant",
                "post",
                None,
                "profile/{profile_id}/loop/{loop_id}/participant",
            ),
            (
                "Participant",
                "patch",
                NotNone,
                "profile/{profile_id}/loop/{loop_id}/participant/{participant_id}",
            ),
            (
                "Participant",
                "delete",
                NotNone,
                "profile/{profile_id}/loop/{loop_id}/participant/{participant_id}",
            ),

            (
                "TaskList",
                "get",
                None,
                "profile/{profile_id}/loop/{loop_id}/tasklist",
            ),
            (
                "TaskList",
                "get",
                NotNone,
                "profile/{profile_id}/loop/{loop_id}/tasklist/{task_list_id}",
            ),

            (
                "Task",
                "get",
                None,
                "profile/{profile_id}/loop/{loop_id}/tasklist/{task_list_id}/task",
            ),
            (
                "Task",
                "get",
                NotNone,
                "profile/{profile_id}/loop/{loop_id}/tasklist/{task_list_id}/task/{task_id}",
            ),

            (
                "Activity",
                "get",
                None,
                "profile/{profile_id}/loop/{loop_id}/activity",
            ),

            ("Contact", "get", None, "contact"),
            ("Contact", "get", NotNone, "contact/{contact_id}"),
            ("Contact", "post", None, "contact"),
            ("Contact", "patch", NotNone, "contact/{contact_id}"),
            ("Contact", "delete", NotNone, "contact/{contact_id}"),

            ("LoopTemplate", "get", None, "profile/{profile_id}/loop-template"),
            (
                "LoopTemplate",
                "get",
                NotNone,
                "profile/{profile_id}/loop-template/{loop_template_id}",
            ),
        ]

    @staticmethod
    def _first(iterable: any) -> any:
        """
        Get the first item from an iterable.

        Args:
            iterable (any): The iterable to get the first item from.

        Returns:
            any: The first item in the iterable.

        Raises:
            KeyError: If the iterable is empty.
        """
        try:
            return next(iter(iterable))
        except StopIteration as e:
            raise KeyError(str(iterable)) from e

    def __getitem__(self, key):
        class_name, method, has_id = key
        logger.debug(
            f"Looking up endpoint for: {class_name}, {method}, has_id={has_id}"
        )
        for item in self._items:
            if (
                item[0] == class_name
                and item[1] == method
                and (
                    (item[2] is None and not has_id) or (item[2] is NotNone and has_id)
                )
            ):
                logger.debug(f"Found endpoint: {item[3]}")
                return item[3]
        logger.error(f"No endpoint found for {class_name}, {method}, has_id={has_id}")
        raise KeyError(f"No endpoint found for {class_name}, {method}, has_id={has_id}")


endpoint_directory = EndpointDirectory()


class DotloopObject:
    BASE_URL = "https://api-gateway.dotloop.com/public/v2/"
    ALLOWED_METHODS = {"delete", "get", "patch", "post"}

    def __init__(self, parent: Optional["DotloopObject"] = None):
        """
        Initialize a DotloopObject.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        self._parent = parent
        self.ID_FIELD: Optional[str] = getattr(self.__class__, "ID_FIELD", None)
        self._id_value: Optional[str] = None
        self._session = getattr(parent, "_session", requests.Session())
        self.endpoint_directory = endpoint_directory
        logger.debug(
            f"{self.__class__.__name__} initialized with ID_FIELD: {self.ID_FIELD}, parent: {parent}"
        )

    def __init_subclass__(cls, id_field: Optional[str] = None, **kwargs):
        """
        Initialize a subclass of DotloopObject.

        Args:
            id_field (Optional[str]): The name of the ID field for this object.
            **kwargs: Additional keyword arguments.
        """
        cls.id_field = id_field
        super().__init_subclass__(**kwargs)

    def __call__(self, id_value: any) -> "DotloopObject":
        """
        Create a new instance of this class with the given ID value.

        Args:
            id_value (any): The ID value to set.

        Returns:
            DotloopObject: A new instance of this class.
        """
        logger.debug(
            f"{self.__class__.__name__}.__call__() called with id_value: {id_value}"
        )
        new_obj = self.__class__(parent=self._parent)
        new_obj._id_value = id_value
        return new_obj

    def collect_ids(self) -> dict[str, Optional[str]]:
        """
        Collect all relevant IDs from this object and its parents.

        Returns:
            A dictionary of ID field names and their values.
        """
        ids = {}
        current = self
        while current is not None:
            if hasattr(current, 'ID_FIELD') and current.ID_FIELD and current.id_value:
                ids[current.ID_FIELD] = current.id_value
            current = getattr(current, '_parent', None)
        return ids

    @property
    def id_value(self) -> Optional[str]:
        return self._id_value

    def __str__(self) -> str:
        """Return a string representation of the object."""
        try:
            if self.id_field is not None:
                return f"<{self.__class__.__name__}({self.id_field}={getattr(self, self.id_field)})>"
            else:
                return f"<{self.__class__.__name__}>"
        except AttributeError:
            return "<DotloopObject>"

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return str(self)

    def __getattr__(self, name: str) -> any:
        """
        Get an attribute from the parent object if it doesn't exist in this object.

        Args:
            name (str): The name of the attribute.

        Returns:
            any: The value of the attribute.

        Raises:
            AttributeError: If the attribute doesn't exist in the parent object.
        """
        if self._parent is not None:
            return getattr(self._parent, name)
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    def delete(self, *args, **kwargs) -> dict:
        """Delete method to be implemented by subclasses."""
        return NotImplemented

    def get(self, *args, **kwargs) -> dict:
        """Get method to be implemented by subclasses."""
        return NotImplemented

    def patch(self, *args, **kwargs) -> dict:
        """Patch method to be implemented by subclasses."""
        return NotImplemented

    def post(self, *args, **kwargs) -> dict:
        """Post method to be implemented by subclasses."""
        return NotImplemented

    def fetch(self, method: str, **kwargs) -> dict[str, any]:
        """
        Fetch data from the Dotloop API.

        Args:
            method (str): The HTTP method to use.
            **kwargs: Additional keyword arguments for the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ValueError: If an invalid HTTP method is provided.
            requests.RequestException: If there's an error with the request.
            JSONDecodeError: If the response cannot be decoded as JSON.
        """
        logger.debug(f"Fetching with method: {method}, class: {self.__class__.__name__}, id_value: {self.id_value}")
        try:
            endpoint: str = self.endpoint_directory[self.__class__.__name__, method, self.id_value is not None]
            logger.debug(f"Endpoint found: {endpoint}")
        except KeyError as e:
            logger.error(f"Endpoint not found: {e}")
            raise

        format_dict = self.collect_ids()
        logger.debug(f"format_dict: {format_dict}")

        try:
            endpoint = endpoint.format(**format_dict)
        except KeyError as e:
            logger.error(f"Failed to format endpoint: {endpoint} with format_dict: {format_dict}")
            raise

        url = urljoin(self.BASE_URL, endpoint)
        logger.debug(f"Constructed URL: {url}")

        if method not in self.ALLOWED_METHODS:
            raise ValueError(f'HTTP allowed methods are {self.ALLOWED_METHODS}, got "{method}".')

        try:
            response = getattr(self._session, method.lower())(url, **kwargs)
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response content: {response.content[:100]}...")  # Log first 100 chars of content
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {'error': 'RequestException', 'message': str(e), 'status': getattr(e.response, 'status_code', None)}
        except JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return {'error': 'JSONDecodeError', 'message': f'{str(e)}: {response.content.decode()}',
                    'status': response.status_code}
