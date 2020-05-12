import pytest
from unittest.mock import patch

from simulert.handlers import Emailer


@pytest.fixture(autouse=True, params=[True, False])
def mock_send(request):
    """The `sendmail` method for a mocked SMTP server class that is patched over the
    server class used in `simulert.handlers.email`."""
    ssl = request.param
    with patch("simulert.handlers.email.SMTP_SSL", set=True) as mock_ssl_server:
        if ssl:
            yield mock_ssl_server().sendmail
        else:
            mock_ssl_server.side_effect = ConnectionRefusedError()
            with patch("simulert.handlers.email.SMTP", set=True) as mock_server:
                yield mock_server().sendmail


def test_constructor_from_args():
    """Test that the email handler instantiates correctly with defined args."""
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
    """Test that the email handler instantiates correctly from environment variables."""
    monkeypatch.setenv("SIMULERT_EMAIL_AUTHENTICATION", "user, key")
    monkeypatch.setenv("SIMULERT_EMAIL_SENDER", "see,sail")
    monkeypatch.setenv("SIMULERT_EMAIL_RECIPIENT", "soo,rail")
    monkeypatch.setenv("SIMULERT_EMAIL_HOST", "proculus")
    monkeypatch.setenv("SIMULERT_EMAIL_PORT", "42")
    handler = Emailer()
    assert handler.authentication == ("user", "key")
    assert handler.sender == ("see", "sail")
    assert handler.recipient == ("soo", "rail")
    assert handler.host == "proculus"
    assert handler.port == 42


@pytest.mark.parametrize(
    "args", [{}, {"authentication": ("user", "key")}, {"sender": ("foo", "foo@email")}]
)
def test_constructor_raises(args, monkeypatch):
    """
    Test that the email handler raises with insufficient arguments and undefined
    environment variables.
    """
    for envvar in Emailer._attr_envvar_map.values():
        monkeypatch.delenv(envvar, raising=False)
    with pytest.raises(ValueError):
        Emailer(**args)


def test_send_message(mock_send):
    """
    Test that `send_email` correctly calls `sendmail` from the email server.
    """
    Emailer(
        authentication="user,key",
        sender=("see", "sail"),
        recipient=("soo", "rail"),
        host="lucius",
        port=1025,
    ).send_email("subject", "body")
    mock_send.assert_called_once()
    assert mock_send.call_args[0][0] == ("see", "sail")
    assert mock_send.call_args[0][1] == ("soo", "rail")
    assert mock_send.call_args[0][2].endswith("body")
    assert "Subject: subject" in mock_send.call_args[0][2]


def test_alert(mock_send):
    """
    Test that `alert` correctly calls `sendmail` from the mail server.
    """
    Emailer(
        authentication="user,key",
        sender=("see", "sail"),
        recipient=("soo", "rail"),
        host="vibius",
        port=1025,
    ).alert("a message")
    mock_send.assert_called_once()
    assert mock_send.call_args[0][0] == ("see", "sail")
    assert mock_send.call_args[0][1] == ("soo", "rail")
    assert mock_send.call_args[0][2].endswith("a message")
    assert "Subject: An update on your simulation" in mock_send.call_args[0][2]


def test_alert_raises(caplog, mock_send):
    """
    Test that `alert` will log a failed attempt to send an email.
    """
    mock_send.side_effect = ValueError("valueerror")
    Emailer(
        authentication="user,key",
        sender=("see", "sail"),
        recipient=("soo", "rail"),
        host="faustus",
        port=1025,
    ).alert("a message")
    assert (
        "Email notification to soo failed with ValueError('valueerror')" in caplog.text
    )


def test_send_test_message(mock_send):
    """
    Test that `send_test_email` correctly calls `sendmail` from the email server.
    """
    Emailer(
        authentication=",",
        sender=("see", "sail"),
        recipient=("soo", "rail"),
        host="manius",
        port=1025,
    ).send_test_email()
    mock_send.assert_called_once()
    assert mock_send.call_args[0][0] == ("see", "sail")
    assert mock_send.call_args[0][1] == ("soo", "rail")
    assert "Subject: Test email" in mock_send.call_args[0][2]
