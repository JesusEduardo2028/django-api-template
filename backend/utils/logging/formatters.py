import logging
import os
from typing import Dict, Any, Type

from pythonjsonlogger import json as jsonlogger

DEFAULT_LOG_MESSAGE_FORMAT = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
LOG_MESSAGE_FORMAT = os.getenv("LOG_FORMAT", default=DEFAULT_LOG_MESSAGE_FORMAT)
LOG_FORMAT_TYPE = os.getenv('LOGGER', default="simple").lower()

USE_JSON_FORMAT = LOG_FORMAT_TYPE == 'json'


class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["level"] = record.levelname.lower()


def get_log_formatter() -> Type[logging.Formatter]:
    return JsonFormatter if USE_JSON_FORMAT else logging.Formatter

LOG_FORMATTER = get_log_formatter()

