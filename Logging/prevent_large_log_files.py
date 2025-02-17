import logging
from logging.handlers import RotatingFileHandler

# Rotating file handler (max 1MB per file, keeps 3 backups)
handler = RotatingFileHandler("rotating.log", maxBytes=1_000_000, backupCount=3)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger = logging.getLogger("RotatingLogger")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Example logging
for i in range(10000):
    logger.info(f"Logging message {i}")