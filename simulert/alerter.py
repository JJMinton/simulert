from collections import defaultdict
from contextlib import contextmanager
from copy import copy
import logging

from simulert.logger import logger
from simulert.handlers.logger import Logger as LoggerHandler


class Alerter:
    """
    A class that provides a range of functionality for defining alert events and 
    triggers a list of handlers when these events occur.
    """

    def __init__(self, name=""):
        self.name = name
        self._default_handler = LoggerHandler(
            logger.getChild(self.name), logging.INFO
        )
        self._handlers = [self._default_handler]

    @property
    def handlers(self):
        return copy(self._handlers)

    def add_handler(self, handler):
        self._handlers.append(handler)
        return self

    def remove_handler(self, handler):
        self._handlers.remove(handler)
        return self

    def remove_default_handler(self):
        self._handlers.remove(self._default_handler)
        return self

    def alert(self, msg):
        for handler in self._handlers:
            handler.alert(msg)

    @contextmanager
    def simulation_alert(self, simulation_name="simulation"):
        """
        This context is designed to wrap a running simulation so that if the simulation
        completes, with or without an error, an alert is triggered.

        Arguments:
            alerter (simulert.Alerter):
            name (str): the name of the simulation for reference in the alerts.
        """
        prefix = "" if not self.name else f"{self.name}: "
        try:
            yield
            self.alert(f"{prefix}{simulation_name} has completed without error.")
        except Exception as err:
            self.alert(
                f"{prefix}{simulation_name} failed to complete because of"
                f" {err.__repr__()}."
            )
            raise err


_alerters = defaultdict(Alerter)

def getAlerter(key: str = ""):
    _alerters[key] = _alerters.get(key, Alerter(key))
    return _alerters[key]