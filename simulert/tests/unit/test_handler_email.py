import pytest
from smtpd import DebuggingServer
import time
from threading import Thread
from unittest.mock import Mock, patch, create_autospec

from simulert.handlers import Emailer


@pytest.fixture(autouse=True)
def mock_send():
    with patch("simulert.handlers.email.SMTP", set=True) as mock_server:
        yield mock_server().sendmail


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


def test_send_message(mock_send):
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


def test_alert(mock_send):
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


def test_alert_raises(caplog, mock_send):
    mock_send.side_effect = ValueError("valueerror")
    Emailer(
        authentication=",",  # smtpd.DebuggingServer doesn't support authentication
        sender=("see", "sail"),
        recipient=("soo", "rail"),
        host="localhost",
        port=1025,
    ).alert("a message")
    assert (
        "Email notification to soo failed with ValueError('valueerror')" in caplog.text
    )


def test_send_test_message(mock_send):
    Emailer(
        authentication=",",  # smtpd.DebuggingServer doesn't support authentication
        sender=("see", "sail"),
        recipient=("soo", "rail"),
        host="localhost",
        port=1025,
    ).send_test_email()
    mock_send.assert_called_once()
    assert mock_send.call_args[0][0] == ("see", "sail")
    assert mock_send.call_args[0][1] == ("soo", "rail")
    assert "Subject: Test email" in mock_send.call_args[0][2]
