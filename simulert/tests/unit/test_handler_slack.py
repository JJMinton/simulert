import pytest
from slack import WebClient
from unittest.mock import Mock, patch, create_autospec

from simulert.handlers import Slacker


def test_constructor_from_args():
    """Test that the slack handler instantiates correctly from arguments."""
    handler = Slacker("grok", "fee")
    assert handler.token == "grok"
    assert handler.username == "fee"
    assert isinstance(handler.client, WebClient)


def test_constructor_from_environ(monkeypatch):
    """Test that the slack handler instantiates correctly from environment variables."""
    monkeypatch.setenv("SIMULERT_SLACK_TOKEN", "foo")
    monkeypatch.setenv("SIMULERT_SLACK_USERNAME", "bar")
    handler = Slacker()
    assert handler.token == "foo"
    assert handler.username == "bar"
    assert isinstance(handler.client, WebClient)


@pytest.mark.parametrize("args", [{}, {"token": "bar"}, {"username": "foo"},])
def test_constructor_raises(args, monkeypatch):
    """Test that the slack handler raises with insufficient arguments and undefined
    environment variables."""
    monkeypatch.delenv("SIMULERT_SLACK_TOKEN", raising=False)
    monkeypatch.delenv("SIMULERT_SLACK_USERNAME", raising=False)
    with pytest.raises(ValueError):
        Slacker(**args)


def test_send_message(monkeypatch):
    """
    Test that `send_message` correctly calls `chat_postMessage` of the slack webclient.
    """
    with patch(
        "simulert.handlers.slack.WebClient.chat_postMessage", set=True
    ) as mock_post:
        Slacker("grok", "fee").send_message("a message")
        mock_post.assert_called_once_with(channel="@fee", text="a message")


def test_alert(monkeypatch):
    """
    Test that `alert` correctly calls `chat_postMessage` of the slack webclient.
    """
    with patch(
        "simulert.handlers.slack.WebClient.chat_postMessage", set=True
    ) as mock_post:
        Slacker("grok", "fee").alert("a message")
        mock_post.assert_called_once_with(channel="@fee", text="a message")


def test_alert_raises(monkeypatch, caplog):
    """
    Test that `alert` logs failed attempts to call `chat_postMessage` of the slack
    webclient.
    """
    with patch(
        "simulert.handlers.slack.WebClient.chat_postMessage", set=True
    ) as mock_post:
        mock_post.side_effect = ValueError("valueerror")
        Slacker("grok", "fee").alert("a message")
        assert (
            "Slack notification to fee failed with ValueError('valueerror')"
            in caplog.text
        )


def test_send_test_message(monkeypatch):
    """
    Test that `send_test_message` correctly calls `chat_postMessage` of the slack
    webclient.
    """
    with patch(
        "simulert.handlers.slack.WebClient.chat_postMessage", set=True
    ) as mock_post:
        Slacker("grok", "fee").send_test_message()
        mock_post.assert_called_once()
