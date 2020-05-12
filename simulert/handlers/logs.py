import logging
from typing import Optional

from simulert.handlers.base_handler import BaseHandler
from simulert.logger import logger as simulerts_logger

logger = simulerts_logger.getChild(__name__)


class Logger(BaseHandler):
    """
    An alert handler that will log alerts.
    """
    def __init__(
        self,
        user_logger: Optional[logging.Logger] = None,
        level: Optional[int]=logging.INFO
    ):
        """
        Arguments:
            user_logger (Optional[logging.Logger]): the logger to log alerts to
                [default: logging.getLogger("simulert.logs")]
            level (Optional[int]): the level at which the alerts will be logged. This
                must be a registered log level. [default: logging.INFO].
        """
        self.user_logger = user_logger or logger
        self.level = level

    def alert(self, message: str):
        """
        Log an alert.
        Arguments:
            message (str): the message to be logged.
        """
        self.user_logger.log(self.level, message)
