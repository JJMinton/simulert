from datetime import datetime
import os
from typing import Optional

from slack import WebClient

from simulert.handlers.base_handler import BaseHandler
from simulert.logger import logger as simulert_logger

logger = simulert_logger.getChild(__name__)


class Slacker(BaseHandler):
    """
    An alert handler that will post alerts to Slack.
    """

    _attr_envvar_map = {
        "token": "SIMULERT_SLACK_TOKEN",
        "username": "SIMULERT_SLACK_USERNAME",
    }

    def __init__(self, token: Optional[str] = None, username: Optional[str] = None):
        """
        Arguments:
            token (Optional[str]): the api token for the slack bot from which alerts
                from this handler will be sent from
                [default: os.environ["SIMULERT_SLACK_TOKEN"]].
            username (Optional[str]): the username the slack message will be sent to
                [default: os.environ[SIMULERT_SLACK_USERNAME]].
        """
        self.token = token or os.environ.get(self._attr_envvar_map["token"])
        self.username = username or os.environ.get(self._attr_envvar_map["username"])
        self.check_valid_args()
        self.client = WebClient(token)

    def send_message(self, message: str):
        """
        Sends a message via slack.
        Arguments:
            message (str): the text of the message to be sent.
        """
        self.client.chat_postMessage(
            channel=f"@{self.username}", text=message,
        )

    def alert(self, message):
        """
        Sends a message via slack with error protection.

        Arguments:
            message (str): the text of the message to be sent.
        """
        try:
            self.send_message(message)
        except Exception as err:
            logger.exception(
                f"Slack notification to {self.username} failed with {err.__repr__()}"
            )

    def send_test_message(self):
        """Sends a test message via slack."""
        self.send_message(f"This test message was sent at {datetime.now()}")
