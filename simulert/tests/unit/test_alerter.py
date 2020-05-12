import pytest

from simulert.alerter import Alerter, getAlerter
from simulert.handlers.logs import Logger

MESSAGE = "ALERT! ALERT! ALERT!"


@pytest.mark.parametrize("name", ("", "foo"))
def test_get_alerter_is_singleton(name):
    """Test that getAlerter will always return the same alerter by the same name."""
    assert getAlerter(name) is getAlerter(name)
    assert getAlerter(name) is not getAlerter("bar")


def test_get_default_alerter():
    """
    Test that the default alerter is returned with the default handler.
    """
    alerter = getAlerter()
    assert alerter is getAlerter()
    assert len(alerter.handlers) == 1
    assert isinstance(alerter.handlers[0], Logger)


def test_alert(mock_handler):
    """
    Test that the alerter propagates alerts to it's handlers.
    """
    alerter = Alerter().remove_default_handler()
    with mock_handler.bind(alerter):
        alerter.alert(MESSAGE)
    assert mock_handler.last_called_with(MESSAGE)


def test_add_remove_handler(mock_handler):
    """
    Test add_handler and remove_handler.
    """
    # Test adding a handler
    alerter = Alerter().add_handler(mock_handler)
    assert mock_handler in alerter.handlers

    # Test removing a handler
    alerter.remove_handler(mock_handler)
    assert mock_handler not in alerter.handlers


def test_remove_default_handler():
    """
    Check that a newly instantiated Alerter has no handlers when the default handler is
    removed.
    """
    assert not Alerter().remove_default_handler().handlers


def test_run_simulation_context(alerter_with_mock_handler, mock_handler):
    """
    Test that the simulation context sends the correct alert on completion.
    """
    with alerter_with_mock_handler.simulation_alert():
        pass
    assert mock_handler.last_called_with(
        "mock: simulation has completed without error."
    )


def test_run_simulation_context_with_error(alerter_with_mock_handler, mock_handler):
    """
    Test that the simulation context sends the correct alert on an error and reraises
    the error.
    """
    reraise = False
    try:
        with alerter_with_mock_handler.simulation_alert():
            raise RuntimeError()
    except RuntimeError:
        reraise = True
    finally:
        assert mock_handler.last_called_with(
            "mock: simulation failed to complete because of RuntimeError()."
        )
        assert reraise
