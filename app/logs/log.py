""" This module contains the log configuration for the input/output of application's routes."""

import logging
import time

from logging.handlers import RotatingFileHandler

class UTCConverter(logging.Formatter):
    """
        This class is used to convert the time to UTC format.
    """
    def __init__(self, format, date_format, style='%'):
        super().__init__(format, date_format, style)

        # set gmtime
        self.converter = time.gmtime
        
    def formatTime(self, record, datefmt):
        ct = self.converter(record.created)
        return time.strftime(datefmt, ct) if datefmt else\
            "%s,%02d" % (time.strftime("%Y-%m-%d %H:%M:%S", ct), record.msecs)

    def get_instance():
        """
            Get the instance of the UTCConverter.
        """
        return UTCConverter(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            date_format='%Y-%m-%d %H:%M:%S %z'
        )

def get_rotating_file_handler():
    """
        Get the rotating file handler.
    """
    return RotatingFileHandler(
        "app/logs/webserver.log",
        maxBytes=5000,
        backupCount=7
    )

def instantiate_logger():
    """
        Instantiate the logger.
    """

    utc_converter = UTCConverter.get_instance()

    handler = get_rotating_file_handler()
    handler.setFormatter(utc_converter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
