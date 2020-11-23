from unittest.mock import patch

import pytest

from simulert.handlers import Pushover


def test_constructor_from_args():
    """Test that the pushover handler instantiates correctly from arguments."""
    handler = Pushover("grok", "fee")
    assert handler.token == "grok"
    assert handler.username == "fee"


def test_constructor_from_environ(monkeypatch):
    """Test that the pushover handler instantiates correctly from environment variables."""
    monkeypatch.setenv("SIMULERT_PUSHOVER_TOKEN", "foo")
    monkeypatch.setenv("SIMULERT_PUSHOVER_USERNAME", "bar")
    handler = Pushover()
    assert handler.token == "foo"
    assert handler.username == "bar"


@pytest.mark.parametrize("args", [{}, {"token": "bar"}, {"username": "foo"}, ])
def test_constructor_raises(args, monkeypatch):
    """Test that the pushover handler raises with insufficient arguments and undefined
    environment variables."""
    monkeypatch.delenv("SIMULERT_PUSHOVER_TOKEN", raising=False)
    monkeypatch.delenv("SIMULERT_PUSHOVER_USERNAME", raising=False)
    with pytest.raises(ValueError):
        Pushover(**args)


def test_send_message(monkeypatch):
    """
    Test that `send_message` correctly calls `chat_postMessage` of the pushover webclient.
    """
    with patch(
        "simulert.handlers.pushover.Pushover._post_to_api", set=True
    ) as mock_post:
        Pushover("grok", "fee").send_message(message="a message")
        mock_post.assert_called_once_with(message="a message")


def test_alert(monkeypatch):
    """
    Test that `alert` correctly calls `chat_postMessage` of the pushover webclient.
    """
    with patch(
        "simulert.handlers.pushover.Pushover._post_to_api", set=True
    ) as mock_post:
        Pushover("grok", "fee").alert("a message")
        mock_post.assert_called_once_with(message="a message")


def test_alert_raises(monkeypatch, caplog):
    """
    Test that `alert` logs failed attempts to call `chat_postMessage` of the pushover
    webclient.
    """
    with patch(
        "simulert.handlers.pushover.Pushover._post_to_api", set=True
    ) as mock_post:
        mock_post.side_effect = ValueError("valueerror")
        Pushover("grok", "fee").alert("a message")
        assert (
            "Pushover notification to fee failed with ValueError('valueerror'"
            in caplog.text
        )


def test_send_test_message(monkeypatch):
    """
    Test that `send_test_message` correctly calls `chat_postMessage` of the pushover
    webclient.
    """
    with patch(
        "simulert.handlers.pushover.Pushover._post_to_api", set=True
    ) as mock_post:
        Pushover("grok", "fee").send_test_message()
        mock_post.assert_called_once()
