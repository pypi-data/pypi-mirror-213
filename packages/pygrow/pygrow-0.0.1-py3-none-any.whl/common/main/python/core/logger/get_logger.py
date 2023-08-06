import sys
import logging


def getLogger():
  # Create a logger for the module
  logger = logging.getLogger(__name__)
  # Set the log level to DEBUG
  logger.setLevel(logging.INFO)

  # Create a formatter with ISO-8601 timestamp
  formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
  # Create a rotating file handler with 10 MB size limit and 10 backup files
  # handler = logging.handlers.RotatingFileHandler(filename='/tmp/myapp.log', maxBytes=10 * 1024 * 1024, backupCount=10)

  handler = logging.StreamHandler(sys.stdout)
  # Set the formatter for the handler
  handler.setFormatter(formatter)

  # Add the handler to the logger
  logger.addHandler(handler)

  return logger


logger = getLogger()
