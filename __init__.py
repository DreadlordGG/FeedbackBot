import os
import sys
import discord
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.logging import getLogger
from core.settings import Config
from core.db import async_pgsql
conf = Config()
class FeedbackBot(commands.AutoShardedBot):
    def __init__(self):
        self.command_prefix='$'
        super().__init__(self.command_prefix)
        self.token = conf.DISCORD_TOKEN
        self.command_prefix=conf.COMMAND_PREFIX
        self.engine = None

    def launch(self):
        db = async_pgsql(conf.DATABASE)
        self.engine = self.loop.run_until_complete(db.create_engine())
        self.load_extension("cogs.events")
        self.load_extension("cogs.admin")
        self.load_extension("cogs.user")      
        self.run(self.token)
