from datetime import datetime
import os

from slack import WebClient

from simulert.handlers.base_handler import BaseHandler
from simulert.logger import logger as simulert_logger

logger = simulert_logger.getChild(__name__)


class Slacker(BaseHandler):

    _attr_envvar_map = {
        "token": "SIMULERT_SLACK_TOKEN",
        "username": "SIMULERT_SLACK_USERNAME",
    }

    def __init__(self, token=None, username=None):
        self.token = token or os.environ.get(self._attr_envvar_map["token"])
        self.username = username or os.environ.get(self._attr_envvar_map["username"])
        self.check_valid_args()
        self.client = WebClient(token)

    def send_message(self, message):
        self.client.chat_postMessage(
            channel=f"@{self.username}", text=message,
        )

    def alert(self, message):
        try:
            self.send_message(message)
        except Exception as err:
            logger.exception(
                f"Slack notification to {self.username} failed with {err.__repr__()}"
            )

    def send_test_message(self):
        self.send_message(f"This test message was sent at {datetime.now()}")
