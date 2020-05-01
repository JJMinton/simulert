import email
import smtplib
from contextlib import contextmanager
from datetime import datetime
from email.mime.text import MIMEText
from typing import Iterable, Union

from simulert.handlers.base_handler import BaseHandler
from simulert.logger import logger as simulert_logger

logger = simulert_logger.getChild(__name__)


class Emailer(BaseHandler):
    def __init__(
        self,
        username: str,
        key: str,
        sender: str,
        recipient: Union[str, Iterable[str]],
        host: str,
        port: int = 587,
    ):
        """
        Arguments:
            username (str):
            key (str):
            host (str):
            port (int): [default: 587]
            sender (int):
            recipient (Union[str, Iterable[str]]):
        """
        self.username = username
        self.key = key
        self.host = host
        self.port = port
        self.sender = sender
        self.recipient = recipient

    @contextmanager
    def _server(self):
        server = smtplib.SMTP(self.host, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.key)
        try:
            yield server
        finally:
            server.quit()

    def send_email(self, subject, body):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["To"] = email.utils.formataddr(self.recipient)
        msg["From"] = email.utils.formataddr(self.sender)
        with self._server() as server:
            server.sendmail(self.sender, self.recipient, msg.as_string())

    def send_test_email(self):
        self.send_email(
            "Test email", f"This test email was sent at {datetime.now()}"
        )

    def alert(self, message):
        try:
            self.send_email("An update on your simulation", message)
        except Exception as err:
            logger.exception(
                f"Email notification to {self.recipients} failed with", err.__repr__()
            )
