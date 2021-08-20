import logging
import sys
import os
class FeedbackbotLogger(logging.Logger):
    @staticmethod
    def _info_(*msgs):
        return f'{Fore.LIGHTMAGENTA_EX}{" ".join(msgs)}{Style.RESET_ALL}'

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../logs/", 'FeedbackBot.log')

print(log_file)
log_level = logging.INFO
fh = logging.FileHandler(log_file)
fh.setLevel(log_level)
loggers = set()
formatter = logging.Formatter(
    "%(asctime)s %(name)s[%(lineno)d] %(funcName)s - %(levelname)s: %(message)s", datefmt="%d/%m/%y %H:%M:%S"
)
fh.setFormatter(formatter)
logging.setLoggerClass(FeedbackbotLogger)

def getLogger(name=None, guild=None) -> FeedbackbotLogger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(fh)
    loggers.add(logger)
    return logger