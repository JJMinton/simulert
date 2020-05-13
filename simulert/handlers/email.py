import email
import os
from smtplib import SMTP, SMTP_SSL
from contextlib import contextmanager
from datetime import datetime
from email.mime.text import MIMEText
from ssl import SSLError
from typing import Iterable, Union, Tuple, Optional

from simulert.handlers.base_handler import BaseHandler
from simulert.logger import logger as simulert_logger

logger = simulert_logger.getChild(__name__)


class Emailer(BaseHandler):
    """
    An alert handler that will send emails.
    """

    _attr_envvar_map = {
        "host": "SIMULERT_EMAIL_HOST",
        "port": "SIMULERT_EMAIL_PORT",
        "authentication": "SIMULERT_EMAIL_AUTHENTICATION",
        "sender": "SIMULERT_EMAIL_SENDER",
        "recipient": "SIMULERT_EMAIL_RECIPIENT",
    }

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        authentication: Optional[Union[str, Tuple[str]]] = None,
        sender: Optional[str] = None,
        recipient: Optional[Union[str, Iterable[str]]] = None,
    ):
        """
        Arguments:
            host (Optional[str]): the address of the mail server to be used to send
                email alerts [default: os.environ["SIMULERT_EMAIL_HOST"]].
            port (Optional[int]): the port of the mail server to be used to send email
                alerts [default: os.environ["SIMULERT_EMAIL_PORT"]].
            authentication (Optional(Union[str, Tuple[str, str]]]): a 2-tuple or a comma
                delimited string defining the username and password of the email server
                to send mail [default: os.environ["SIMULERT_EMAIL_AUTHENTICATION"]].
            sender (Optional[str]): a comma delimited string defining the name and email
                address of the sender of the email alert
                [default: os.environ["SIMULERT_EMAIL_SENDER"]].
            recipient (Optional[Union[str, Iterable[str]]]): a comma delimited string or
                list of comma delimited strings defining the name(s) and email(s) of the
                recipients of email alerts
                [default: os.environ["SIMULERT_EMAIL_RECIPIENT"]].
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
        """A convenience context that connects to an SMTP server."""
        try:
            server = SMTP_SSL(self.host, self.port)
        except (SSLError, ConnectionRefusedError):
            logger.warning("Using a non TSL server connection.")
            server = SMTP(self.host, self.port)
        try:
            server.ehlo()
            if self.authentication[0]:
                server.login(*self.authentication)
            yield server
        finally:
            server.quit()

    def send_email(self, subject: str, body: str):
        """
        Sends an email with the provided subject and body.
        Arguments:
            subject (str): the email's subject.
            body (str): the email's text content.
        """
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["To"] = email.utils.formataddr(self.recipient)
        msg["From"] = email.utils.formataddr(self.sender)
        with self._server() as server:
            server.sendmail(self.sender, self.recipient, msg.as_string())

    def alert(self, message: str):
        """
        Sends an email with error protection. The subject of the email will be "An
        update on your simulation."

        Arguments:
            message (str): text for the content of the email.
        """
        try:
            self.send_email("An update on your simulation", message)
        except Exception as err:
            logger.exception(
                f"Email notification to {self.recipient[0]} failed with"
                f" {err.__repr__()}"
            )

    def send_test_email(self):
        """Sends a test email."""
        self.send_email("Test email", f"This test email was sent at {datetime.now()}")
