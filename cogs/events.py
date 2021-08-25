from discord.ext import commands
from core.logging import getLogger
logger = getLogger(__name__)
import discord
from core.db import async_pgsql
from core.models import Server
from sqlalchemy.dialects.postgresql import insert

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Feedback"))
        logger.info(f"FeedbackBot is up and running")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True,send_messages=True)
    }
        admin_channel = discord.utils.get(guild.text_channels, name='feedback-admin')
        if admin_channel is None:
            await guild.create_text_channel('feedback-admin', overwrites=overwrites)

        async with self.bot.engine.connect() as conn:
            stmt = (
                insert(Server).
                values(guild=guild.id).on_conflict_do_nothing()
            )
            result = await conn.execute(stmt)
        logger.info(f'[{guild.name}] Setup done...')
        
def setup(bot):
    bot.add_cog(Events(bot))