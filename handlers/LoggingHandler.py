import logging
from datetime import datetime
import pytz
import re


class RacuFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.timezone = pytz.timezone('US/Eastern')

    def format(self, record):
        message = record.getMessage()
        message = re.sub(r'\n', '', message)  # Remove newlines
        message = re.sub(r'\s+', ' ', message)  # Remove multiple spaces
        message = message.strip()  # Remove leading and trailing spaces

        record.msg = message
        return super().format(record)

    def formatTime(self, record, datefmt=None):
        timestamp = self.timezone.localize(datetime.fromtimestamp(record.created))
        if datefmt:
            return timestamp.strftime(datefmt)
        else:
            return str(timestamp)


def setup_logger():

    # Initialize the logger
    logger = logging.getLogger('Racu.Core')

    if logger.handlers:
        # Handlers already exist, no need to add more
        return logger

    logger.setLevel(logging.DEBUG)

    # Create console handler and set level and formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = RacuFormatter('[%(asctime)s] [%(name)s] %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.propagate = False
    logging.captureWarnings(True)

    return logger