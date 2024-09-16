import logging
from typing import Optional, Generator

from .bases import DotloopObject
from .loop import Loop
from .loop_it import LoopIt
from .loop_template import LoopTemplate

logger = logging.getLogger(__name__)

class Profile(DotloopObject):
    """Represents a profile in the Dotloop API."""
    ID_FIELD = 'profile_id'

    def __init__(self, parent: Optional[DotloopObject] = None):
        """
        Initialize a Profile object.

        Args:
            parent (Optional[DotloopObject]): The parent object, if any.
        """
        super().__init__(parent)
        logger.debug(f"Profile initialized with parent: {parent}, id_value: {self._id_value}")

    def __call__(self, profile_id: str) -> 'Profile':
        """
        Allow setting the profile_id using method chaining.

        Args:
            profile_id (str): The ID of the profile to retrieve.

        Returns:
            Profile: A new Profile instance with the specified profile_id.
        """
        logger.debug(f"Profile.__call__() called with profile_id: {profile_id}")
        new_profile = super().__call__(profile_id)
        logger.debug(f"New Profile created with id_value: {new_profile.id_value}")
        return new_profile

    @property
    def loop(self) -> Loop:
        """
        Get a Loop object associated with this profile.

        Returns:
            Loop: A Loop object.
        """
        return Loop(parent=self)

    @property
    def loop_it(self) -> LoopIt:
        """
        Get a LoopIt object associated with this profile.

        Returns:
            LoopIt: A LoopIt object.
        """
        return LoopIt(parent=self)

    @property
    def loop_template(self) -> LoopTemplate:
        """
        Get a LoopTemplate object associated with this profile.

        Returns:
            LoopTemplate: A LoopTemplate object.
        """
        return LoopTemplate(parent=self)

    def get(self, batch_size: int = 100) -> dict[str, any]:
        """
        Retrieve profile information for a single profile.

        Returns:
            dict[str, any]: The profile information.
        """
        logger.debug(f"Profile.get() called with id_value: {self.id_value}")
        return self.fetch('get')

    def get_all(self, batch_size: int = 100) -> Generator[dict[str, any], None, None]:
        """
        Retrieve all profiles, handling pagination.

        Args:
            batch_size (int): Number of profiles to retrieve per request. Max is 100.

        Yields:
            dict[str, any]: Profile information for each profile.
        """
        batch_number = 1
        total_profiles = None
        profiles_fetched = 0

        while total_profiles is None or profiles_fetched < total_profiles:
            logger.debug(f"Fetching profiles batch {batch_number} with size {batch_size}")
            params = {
                'batch_number': batch_number,
                'batch_size': min(batch_size, 100)  # Ensure batch_size doesn't exceed 100
            }
            response = self.fetch('get', params=params)

            if total_profiles is None:
                total_profiles = response.get('meta', {}).get('total')
                logger.debug(f"Total profiles to fetch: {total_profiles}")

            profiles = response.get('data', [])
            for profile in profiles:
                yield profile
                profiles_fetched += 1

            if len(profiles) < batch_size:
                break

            batch_number += 1

    def post(self, **kwargs: any) -> dict[str, any]:
        """
        Create a new profile.

        Args:
            **kwargs: The profile fields for the new profile.

        Returns:
            dict[str, any]: The newly created profile information.

        Raises:
            DotloopAPIException: If there's an error creating the profile.
        """
        return self.fetch('post', json=kwargs)

    def patch(self, **kwargs: any) -> dict[str, any]:
        """
        Update the profile information.

        Args:
            **kwargs: The profile fields to update.

        Returns:
            dict[str, any]: The updated profile information.

        Raises:
            DotloopAPIException: If there's an error updating the profile information.
        """
        return self.fetch('patch', json=kwargs)
