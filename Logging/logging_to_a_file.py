import logging

#Creates app.log and writes logs to it.
# logging.basicConfig(filename='app.log', level=logging.INFO)
 logging.basicConfig (filename='app.log', level=logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s") 
#%(asctime)s adds a timestamp, %(levelname)s adds the log level, and %(message)s logs the actual message.
logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")

