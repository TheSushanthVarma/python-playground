import logging

logging.basicConfig(level=logging.INFO)

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")

# Only WARNING, ERROR, and CRITICAL messages appear in the console.

for i in range(10):
    logging.info(f"This is an info message {i}")

    if i == 5:
        logging.warning("This is a warning message")

    if i == 7:
        logging.error("This is an error message")

    if i == 9:
        logging.critical("This is a critical message")

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.error("Error: %s", e)








