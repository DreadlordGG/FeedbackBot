import os
import discord
import sys
from dotenv import load_dotenv
from FeedbackBot import FeedbackBot
def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    Bot = FeedbackBot(TOKEN)
    Bot.run()

if __name__ == '__main__':  # for `python -m` invocation
    main()