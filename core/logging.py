import logging
import sys
import os

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../logs/", 'FeedbackBot.log')
log_level = logging.INFO
fh = logging.FileHandler(log_file)
fh.setLevel(log_level)
loggers = set()
formatter = logging.Formatter(
    "%(asctime)s %(name)s[%(lineno)s][%(funcName)s] - %(levelname)s: %(message)s", datefmt="%d/%m/%y %H:%M:%S"
)
fh.setFormatter(formatter)
logging.setLoggerClass(logging.Logger)

def getLogger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(fh)
    loggers.add(logger)
    return logger