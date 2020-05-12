from contextlib import contextmanager

import pytest

from simulert.alerter import Alerter
from simulert.handlers.base_handler import BaseHandler


class MockHandler(BaseHandler):
    """
    A mock alert handler that capture messages and provides a convenience context for
    registering it with an alerter.
    """

    def __init__(self):
        self._messages = []

    def alert(self, message):
        self._messages.append(message)

    @contextmanager
    def bind(self, alerter):
        alerter.add_handler(self)
        try:
            yield
        finally:
            alerter.remove_handler(self)

    def called_with(self, message):
        return message in self._messages

    def last_called_with(self, message):
        return bool(self._messages) and (self._messages[-1] == message)


@pytest.fixture
def mock_handler():
    """
    An instance of a mock alert handler.
    """
    return MockHandler()


@pytest.fixture
def alerter_with_mock_handler(mock_handler):
    """
    An alerter with the default handler replaced with a mock handler.
    """
    return Alerter("mock").remove_default_handler().add_handler(mock_handler)
