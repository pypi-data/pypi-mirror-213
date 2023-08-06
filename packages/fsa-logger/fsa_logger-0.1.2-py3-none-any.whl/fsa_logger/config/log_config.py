import logging
from logging.config import dictConfig

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    # LOGGER_NAME: str = "root"
    LOGGER_NAME: str = "fsa_logger"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | [%(name)s] %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }

lc = LogConfig()
dictConfig(lc.dict())
logger = logging.getLogger(lc.LOGGER_NAME)
logger.setLevel(logging.DEBUG)
