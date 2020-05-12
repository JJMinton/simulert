from abc import ABC, abstractmethod


class BaseHandler(ABC):
    """
    A base alert handler: a class that defines methods for sending alerts as a result
    of simulation events being detected.
    """

    _attr_envvar_map = {}  # A dictionary of argument names to environment variables

    @abstractmethod
    def alert(self, message: str):
        """Send an alert.
        Arguments:
            message (str): The message the alert should contain.
        """

    def check_valid_args(self):
        """Utilitly method that checks whether each argument defined in
        `_attr_envvar_map` was defined and raises if any weren't.

        Raises:
            (ValueError): an error reporting which missing arguments were not defined.
        """

        missing_args = {
            attr_name
            for attr_name in self._attr_envvar_map
            if getattr(self, attr_name) is None
        }
        if missing_args:
            raise ValueError(
                f"This handler was instantiated without {missing_args}. These can be"
                " defined as arguments to the constructor or with the following"
                " arguments:\n"
                + "\n".join(
                    [f"{key}: {self._attr_envvar_map[key]}" for key in missing_args]
                )
            )
