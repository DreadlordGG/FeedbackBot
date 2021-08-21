import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import discord
from dotenv import load_dotenv
from discord.ext import commands
from core.logging import getLogger
logger = getLogger(__name__)
from core.db import pgsql
class FeedbackBot:
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN
        self.bot = discord.AutoShardedClient()
        self.init_setup()

    def init_setup(self):

        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Feedback"))
            logger.info("I am ready to act")

        @self.bot.event
        async def on_guild_join(guild):
            database_name = ''.join(filter(str.isalnum, guild.name))
            db = pgsql(database_name)
            db.init
            overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True,send_messages=True)
        }
            admin_channel = discord.utils.get(guild.text_channels, name='feedback-control')
            general_channel = discord.utils.get(guild.text_channels, name='feedback')
            if admin_channel is None:
               await guild.create_text_channel('feedback-control', overwrites=overwrites)
            logger.info(f'[{guild.name}] Setup done...')

    def run(self):
        self.bot.run(self.TOKEN)