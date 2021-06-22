import logging
import time


LOGGER_NAME = __package__


class UTCTimeFormatter(logging.Formatter):
    converter = time.gmtime


def get_formatter():
    return UTCTimeFormatter("%(asctime)s,%(levelname)s,%(module)s,%(message)s")


def get_logger():
    handler = logging.StreamHandler()
    handler.setFormatter(get_formatter())
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger(LOGGER_NAME)
    logger.addHandler(handler)
    logger.level = logging.INFO
    return logger
