import email
import os
from smtplib import SMTP, SMTP_SSL
from contextlib import contextmanager
from datetime import datetime
from email.mime.text import MIMEText
from typing import Iterable, Union, Tuple

from simulert.handlers.base_handler import BaseHandler
from simulert.logger import logger as simulert_logger

logger = simulert_logger.getChild(__name__)


class Emailer(BaseHandler):

    _attr_envvar_map = {
        "authentication": "SIMULERT_EMAIL_AUTHENTICATION",
        "sender": "SIMULERT_EMAIL_SENDER",
        "recipient": "SIMULERT_EMAIL_RECIPIENT",
        "host": "SIMULERT_EMAIL_HOST",
        "port": "SIMULERT_EMAIL_PORT",
    }

    def __init__(
        self,
        authentication: Tuple[str] = None,
        sender: str = None,
        recipient: Union[str, Iterable[str]] = None,
        host: str = None,
        port: int = None,
    ):
        """
        Arguments:
            authentication (Tuple[str, str]):
            host (str):
            port (int): [default: 587]
            sender (int):
            recipient (Union[str, Iterable[str]]):
        """
        self.authentication = authentication or os.environ.get(
            self._attr_envvar_map["authentication"]
        )
        if isinstance(self.authentication, str):
            self.authentication = tuple(
                s.strip() for s in self.authentication.split(",")
            )
        self.sender = sender or os.environ.get(self._attr_envvar_map["sender"])
        if isinstance(self.sender, str):
            self.sender = tuple(s.strip() for s in self.sender.split(","))
        self.recipient = recipient or os.environ.get(self._attr_envvar_map["recipient"])
        if isinstance(self.recipient, str):
            self.recipient = tuple(s.strip() for s in self.recipient.split(","))
        self.host = host or os.environ.get(self._attr_envvar_map["host"])
        self.port = port or os.environ.get(self._attr_envvar_map["port"])
        self.check_valid_args()
        self.port = int(self.port)

    @contextmanager
    def _server(self):
        try:
            server = SMTP_SSL(self.host, self.port)
        except:
            logger.warning("Using a non TSL server connection.")
            server = SMTP(self.host, self.port)
        try:
            server.ehlo()
            if self.authentication[0]:
                server.login(*self.authentication)
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
        self.send_email("Test email", f"This test email was sent at {datetime.now()}")

    def alert(self, message):
        try:
            self.send_email("An update on your simulation", message)
        except Exception as err:
            logger.exception(
                f"Email notification to {self.recipient[0]} failed with {err.__repr__()}"
            )
