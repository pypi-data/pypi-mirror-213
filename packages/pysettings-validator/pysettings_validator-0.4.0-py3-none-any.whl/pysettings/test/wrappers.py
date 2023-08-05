from typing import Any, List
from ..base import BaseSettings


class SettingsWrapper:
    """This class is meant only for testing purposes and you can use it to wrap a settings object
    and restore its original state after the test is completed.

    Usage:
        # Get your application settings
        from app.conf import settings

        # Wrap the settings object in a new instance of SettingsWrapper
        wrapper = SettingsWrapper(settings)

        # Change any value you want in the settings object
        wrapper.DATABASE_URL = "sqlite://"

        # When you finish, restore original values
        wrapper.finalize()
    """

    def __init__(self, settings: BaseSettings) -> None:
        """
        Initializes a new instance of the SettingsWrapper class.

        Args:
            settings (BaseSettings): The settings object to wrap.

        Returns:
            None.
        """
        self._settings = settings
        self._to_restore: List[Any] = []

    def __setattr__(self, attr: str, value) -> None:
        """Overrides the default setattr behavior to track changes made to the wrapped
        settings object. Only internal attributes are set without tracking.

        Args:
            attr (str): The name of the attribute to set.
            value: The value to set the attribute to.

        Returns:
            None.
        """
        if attr in ["_settings", "_to_restore"]:
            object.__setattr__(self, attr, value)
        else:
            if hasattr(self._settings, attr):
                old_value = getattr(self._settings, attr)
                override = (attr, old_value)
                self._to_restore.append(override)
            setattr(self._settings, attr, value)

    def __getattr__(self, attr: str):
        """
        Overrides the default getattr behavior to return the value of the attribute from the wrapped
        settings object. Settings attributes are retrieved using a proxy to the settings `Option`
        object.

        Args:
            attr (str): The name of the attribute to get.

        Returns:
            Any: The value of the attribute from the wrapped settings object.
        """
        return getattr(self._settings, attr)

    def finalize(self) -> None:
        """Restores the original values of the wrapped settings object.
        This method iterates over the list of attribute overrides that were tracked during the lifetime
        of the wrapper object and restores each attribute to its original value.

        Args:
            None.

        Returns:
            None.
        """
        # Use `reversed` to restore original values in the inverse order they were overridden,
        # ensuring the correct order of value restoration.
        for override in reversed(self._to_restore):
            setattr(self._settings, *override)

        self._to_restore.clear()
