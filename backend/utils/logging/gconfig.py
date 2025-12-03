from utils.logging import formatters, loggers

accesslog = "-"
errorlog = "-"
loglevel = "info"

if formatters.USE_JSON_FORMAT:
    logger_class = loggers.JsonLogger
