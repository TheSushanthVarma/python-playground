import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "detailed"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "configurable.log",
            "level": "INFO",
            "formatter": "detailed"
        }
    },
    "loggers": {
        "customLogger": {
            "level": "DEBUG",
            "handlers": ["console", "file"]
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("customLogger")

logger.debug("Debug log")    # Shown in console only
logger.info("Info log")      # Shown in console and file
logger.warning("Warning log")  # Shown in console and file
