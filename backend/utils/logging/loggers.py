import logging
import sys

from gunicorn.glogging import Logger

from utils.logging.formatters import LOG_MESSAGE_FORMAT, JsonFormatter


class JsonLogger(Logger):
    def setup(self, cfg: dict):
        super().setup(cfg)

        self.__remove_all_existing_loggers()
        json_formatter = JsonFormatter(LOG_MESSAGE_FORMAT)
        handler = self.__setup_log_handler(json_formatter)
        self.__setup_loggers(handler)

    def __remove_all_existing_loggers(self):
        self.error_log.handlers.clear()
        self.access_log.handlers.clear()

    def __setup_log_handler(self, formatter: logging.Formatter):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        return handler

    def __setup_loggers(self, handler: logging.Handler):
        self.access_log.setLevel(logging.INFO)
        self.access_log.addHandler(handler)

        self.error_log.setLevel(logging.INFO)
        self.error_log.addHandler(handler)
