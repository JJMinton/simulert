from simulert.handlers.base_handler import BaseHandler
from simulert.logger import logger as simulerts_logger

logger = simulerts_logger.getChild(__name__)


class Logger(BaseHandler):
    def __init__(self, user_logger, level):
        self.user_logger = user_logger
        self.level = level

    def alert(self, msg):
        self.user_logger.log(self.level, msg)
