import logging
from datetime import datetime
import pytz
import re
import os


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

    logs_folder = 'logs'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    
    debug_log_file = os.path.join(logs_folder, 'debug.log')

    with open(debug_log_file, 'w') as f:
        pass

    # Initialize the logger
    logger = logging.getLogger('Racu.Core')

    if logger.handlers:
        # Handlers already exist, no need to add more
        return logger
    
    logger.setLevel(logging.DEBUG)

    # CONSOLE HANDLER
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = RacuFormatter('[%(asctime)s] [%(name)s] %(message)s',
                                                                        datefmt='%Y-%m-%d %H:%M:%S')

    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # DEBUG LOG TO FILE HANDLER
    debug_file_handler = logging.FileHandler(debug_log_file)
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_formatter = RacuFormatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                                                                            datefmt='%Y-%m-%d %H:%M:%S')
    debug_file_handler.setFormatter(debug_file_formatter)
    logger.addHandler(debug_file_handler)

    logger.propagate = False
    logging.captureWarnings(True)

    return logger