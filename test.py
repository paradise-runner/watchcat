from logger import get_logger
import time


logger = get_logger()

logger.debug('log 1')
time.sleep(1)
logger.info('log 2')