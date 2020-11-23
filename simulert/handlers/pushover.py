import os
from datetime import datetime
from http.client import HTTPSConnection, HTTPResponse
from typing import Optional
from urllib.parse import urlencode

from simulert.handlers.base_handler import BaseHandler
from simulert.logger import logger as simulert_logger

logger = simulert_logger.getChild(__name__)


class Pushover(BaseHandler):
    """
    An alert handler that will push alerts to smart phones using the Pushover app (see pushover.net).
    """

    _attr_envvar_map = {
        "token": "SIMULERT_PUSHOVER_TOKEN",  # corresponds to APP_TOKEN in the example code on pushover.net
        "username": "SIMULERT_PUSHOVER_USERNAME",  # corresponds to USER_TOKEN in the example code on pushover.net
    }

    def __init__(self, token: Optional[str] = None, username: Optional[str] = None):
        """
        Arguments:
            token (Optional[str]): the api token for the pushover service from which alerts
                from this handler will be sent
                [default: os.environ["SIMULERT_PUSHOVER_TOKEN"]].
            username (Optional[str]): the pushover user the message will be sent to
                [default: os.environ[SIMULERT_PUSHOVER_USERNAME]].
        """
        self.token = token or os.environ.get(self._attr_envvar_map["token"])
        self.username = username or os.environ.get(self._attr_envvar_map["username"])
        self.check_valid_args()

    def _post_to_api(self, message: str) -> HTTPResponse:
        conn = HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urlencode({
                         "token": self.token,
                         "user": self.username,
                         "message": message,
                     }), {"Content-type": "application/x-www-form-urlencoded"})
        return conn.getresponse()

    def send_message(self, message: str) -> None:
        """
        Sends a message via pushover.
        Arguments:
            message (str): the text of the message to be sent.
        """
        self._post_to_api(message=message)

    def alert(self, message: str) -> None:
        """
        Sends a message via pushover with error protection.

        Arguments:
            message (str): the text of the message to be sent.
        """
        try:
            self.send_message(message)
        except Exception as err:
            logger.exception(
                f"Pushover notification to {self.username} failed with {err.__repr__()}"
            )

    def send_test_message(self):
        """Sends a test message via pushover."""
        self.send_message(f"This test message was sent at {datetime.now()}")
