from simulert.alerter import getAlerter, Alerter
from simulert.handlers.logs import Logger


MESSAGE = "ALERT! ALERT! ALERT!"

def test_get_default_alerter():
   alerter = getAlerter()
   # Assert repeat calls return the same object
   assert alerter is getAlerter() 

   assert len(alerter.handlers) == 1
   assert isinstance(alerter.handlers[0], Logger)

def test_get_non_default_alerter():
    alerter = getAlerter("foo")
    assert alerter is getAlerter("foo")
    assert alerter is not getAlerter("bar")
    assert alerter is not getAlerter()

def test_alert(mock_handler):
    alerter = Alerter().remove_default_handler()
    with mock_handler.bind(alerter):
        alerter.alert(MESSAGE)
    assert mock_handler.last_called_with(MESSAGE)
    
def test_add_remove_handler(mock_handler):
    #Test adding a handler
    alerter = Alerter().add_handler(mock_handler)
    assert mock_handler in alerter.handlers

    #Test removing a handler
    alerter.remove_handler(mock_handler)
    assert mock_handler not in alerter.handlers

def test_remove_default_handler():
    """
    Check that a newly instantiated Alerter has no handlers when the default handler is
    removed.
    """
    assert not Alerter().remove_default_handler().handlers

def test_run_simulation_context(alerter_with_mock_handler, mock_handler):
    with alerter_with_mock_handler.simulation_alert():
        pass
    assert mock_handler.last_called_with("mock: simulation has completed without error.")

def test_run_simulation_context_with_error(alerter_with_mock_handler, mock_handler):
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
