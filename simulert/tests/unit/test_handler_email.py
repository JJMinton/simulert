import pytest
from smtpd import DebuggingServer
import time
from threading import Thread
from unittest.mock import Mock, patch, create_autospec

from simulert.handlers import Emailer


class SMTPServerThread(Thread):
    def __init__(self):
        super().__init__()
        self.host_port = None

    def run(self):
        self.smtp = DebuggingServer(("127.0.0.1", 0), None)
        self.host_port = self.smtp.socket.getsockname()
        asyncore.loop(timeout=0.1)

    def close(self):
        self.smtp.close()


@pytest.fixture
def dummy_server():
    print("starting server thread")
    server_thread = SMTPServerThread()
    server_thread.start()
    while server_thread.host_port is None:
        time.sleep(0.1)
    host, port = server_thread.host_port
    yield {"host": host, "port": port}
    server_thread.close()
    server_thread.join(10)
    if server_thread.is_alive():
        raise RuntimeError("SMTP Debugging server didn't close in 10sec.")


def test_constructor_from_args():
    handler = Emailer(
        authentication=("user", "key"),
        sender=("see", "sail"),
        recipient=("soo", "rail"),
        host="hostus",
        port=42,
    )
    assert handler.authentication == ("user", "key")
    assert handler.sender == ("see", "sail")
    assert handler.recipient == ("soo", "rail")
    assert handler.host == "hostus"
    assert handler.port == 42


def test_constructor_from_environ(monkeypatch):
    monkeypatch.setenv("SIMULERT_EMAIL_AUTHENTICATION", "user, key")
    monkeypatch.setenv("SIMULERT_EMAIL_SENDER", "see,sail")
    monkeypatch.setenv("SIMULERT_EMAIL_RECIPIENT", "soo,rail")
    monkeypatch.setenv("SIMULERT_EMAIL_HOST", "mostus")
    monkeypatch.setenv("SIMULERT_EMAIL_PORT", "42")
    handler = Emailer()
    assert handler.authentication == ("user", "key")
    assert handler.sender == ("see", "sail")
    assert handler.recipient == ("soo", "rail")
    assert handler.host == "mostus"
    assert handler.port == 42


@pytest.mark.parametrize(
    "args", [{}, {"authentication": ("user", "key")}, {"sender": ("foo", "foo@email")},]
)
def test_constructor_raises(args, monkeypatch):
    for envvar in Emailer._attr_envvar_map.values():
        monkeypatch.delenv(envvar, raising=False)
    with pytest.raises(ValueError):
        Emailer(**args)


def test_send_message(monkeypatch):
    with patch("simulert.handlers.email.SMTP.sendmail", set=True) as mock_send:
        Emailer(
            authentication=",",  # smtpd.DebuggingServer doesn't support authentication
            sender=("see", "sail"),
            recipient=("soo", "rail"),
            host="localhost",
            port=1025,
        ).send_email("subject", "body")
        mock_send.assert_called_once()
        assert mock_send.call_args[0][0] == ("see", "sail")
        assert mock_send.call_args[0][1] == ("soo", "rail")
        assert mock_send.call_args[0][2].endswith("body")
        assert "Subject: subject" in mock_send.call_args[0][2]


def test_alert(monkeypatch):
    with patch("simulert.handlers.email.SMTP.sendmail", set=True) as mock_send:
        Emailer(
            authentication=",",  # smtpd.DebuggingServer doesn't support authentication
            sender=("see", "sail"),
            recipient=("soo", "rail"),
            host="localhost",
            port=1025,
        ).alert("a message")
        mock_send.assert_called_once()
        assert mock_send.call_args[0][0] == ("see", "sail")
        assert mock_send.call_args[0][1] == ("soo", "rail")
        assert mock_send.call_args[0][2].endswith("a message")
        assert "Subject: An update on your simulation" in mock_send.call_args[0][2]


def test_alert_raises(caplog, monkeypatch):
    with patch("simulert.handlers.email.SMTP.sendmail", set=True) as mock_send:
        mock_send.side_effect = ValueError("valueerror")
        Emailer(
            authentication=",",  # smtpd.DebuggingServer doesn't support authentication
            sender=("see", "sail"),
            recipient=("soo", "rail"),
            host="localhost",
            port=1025,
        ).alert("a message")
        assert (
            "Email notification to soo failed with ValueError('valueerror')"
            in caplog.text
        )


def test_send_test_message(monkeypatch, dummy_server):
    print("testing")
    with patch("simulert.handlers.email.SMTP.sendmail", set=True) as mock_send:
        print("mocked sendmail")
        emailer = Emailer(
            authentication=",",  # smtpd.DebuggingServer doesn't support authentication
            sender=("see", "sail"),
            recipient=("soo", "rail"),
            host="localhost",
            port=1025,
        )
        emailer.send_test_email()
        print("alerted")
        mock_send.assert_called_once()
        assert mock_send.call_args[0][0] == ("see", "sail")
        assert mock_send.call_args[0][1] == ("soo", "rail")
        assert "Subject: Test email" in mock_send.call_args[0][2]
