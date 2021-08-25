from dotenv import load_dotenv
from FeedbackBot import FeedbackBot
from core.logging import getLogger
import os
from core.settings import Config
conf = Config()
logger = getLogger(__name__)
def main():
    load_dotenv()
    Bot = FeedbackBot()
    Bot.launch()
      
if __name__ == '__main__':  # for `python -m` invocation
    main()
