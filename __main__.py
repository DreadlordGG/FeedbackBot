import os
import discord
import sys
from dotenv import load_dotenv
from FeedbackBot import FeedbackBot

def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    guild = os.getenv('DISCORD_SERVER')
    database = 'FeedbackBot/backends/FeedbackBot.db'
    Bot = FeedbackBot(TOKEN, database)
    Bot.run()

if __name__