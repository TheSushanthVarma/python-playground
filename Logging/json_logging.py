import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_message = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name
        }
        return json.dumps(log_message)

# Create a logger
logger = logging.getLogger("json_logger")
logger.setLevel(logging.DEBUG)

# JSON File Handler
file_handler = logging.FileHandler("logs.json")
file_handler.setFormatter(JSONFormatter())

logger.addHandler(file_handler)

logger.info("This log is in JSON format")
logger.debug("This is a debug message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
