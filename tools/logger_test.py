import logging
import unittest
from logger import get_logger

import coverage


class TestLogger(unittest.TestCase):
    def test_get_logger(self):
        logger = get_logger('app',log_path='./logs/app.log',log_level=logging.DEBUG)
        logger.debug("This is a debug message.")
        logger.info("This is an info message.")
        logger.warning("This is a warning message.")
        logger.error("This is an error message.")
        logger.critical("This is a critical message.")

    def test_exception(self):
        logger = get_logger('app', log_path='./logs/app.log', log_level=logging.DEBUG)
        try:
            raise ValueError("This is an exception message.")
        except ValueError as e:
            logger.exception(e)