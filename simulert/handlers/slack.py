from datetime import datetime

from slack import WebClient

from simulert.handlers.base_handler import BaseHandler
from simulert.logger import logger as simulert_logger

logger = simulert_logger.getChild(__name__)


class Slacker(BaseHandler):
    def __init__(self, token, username):
        self.client = WebClient(token)  # os.environ["SLACK_API_TOKEN"]
        self.username = username

    def send_message(self, message):
        self.client.chat_postMessage(
            channel=f"@{self.username}", text=message,
        )

    def alert(self, message):
        try:
            self.send_message(message)
        except Exception as err:
            logger.exception(
                f"Email notification to {self.recipients} failed with", err.__repr__()
            )

    def send_test_message(self):
        self.send_message(f"This test message was sent at {datetime.now()}")
