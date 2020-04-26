from abc import ABC, abstractmethod


class BaseHandler(ABC):
    """
    A base alert handler: a class that defines methods for sending alerts as a result
    of simulation events being detected.
    """

    @abstractmethod
    def alert(self, message:str):
        """Send an alert.
        Arguments:
            message (str): The message the alert should contain.
        """
