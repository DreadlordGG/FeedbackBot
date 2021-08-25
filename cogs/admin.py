from discord.ext import commands
from core.logging import getLogger
logger = getLogger(__name__)
import discord
import asyncio
from sqlalchemy.future import select
from core.models import General
import datetime
import humanize
import psutil
import platform
import os
from core.models import Base
from discord import Color

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def uptime(self, ctx):
        async with ctx.bot.engine.connect() as conn:
            stmt = (
                select(General)
            )
            result = await conn.execute(stmt)
            start_time = result.fetchone()._asdict()['start_time']
            uptime = humanize.precisedelta(datetime.datetime.now() - start_time)

            return uptime

    @commands.command(
        description=f"Displays host information about the bot.",
        usage=f"",
    )    
    async def info(self, ctx):
        version_info = '.'.join(str(v) for v in ctx.bot.engine.dialect.server_version_info)
        db_info = f'{ctx.bot.engine.dialect.name} {version_info} with {ctx.bot.engine.dialect.driver} driver'
        db_pool_info = f'Pool size: {ctx.bot.engine.pool.size()}\n  Connections in pool: {ctx.bot.engine.pool.checkedin()}\n Current Overflow: {ctx.bot.engine.pool.overflow()}\n Current Checked out connections:  {ctx.bot.engine.pool.checkedout()}'
        uptime = await self.uptime(ctx)
        embedInfo = discord.Embed(title=ctx.me, description="Information", color=Color.teal())
        embedInfo.add_field(name="Host", value=f'{platform.platform()}', inline=False)
        embedInfo.add_field(name="PID", value=f'{os.getpid()}', inline=False)
        embedInfo.add_field(name="Uptime", value=f'{uptime}', inline=False)
        embedInfo.add_field(name="Python version", value=f'{platform.python_version()}', inline=False)
        embedInfo.add_field(name="CPU Usage", value=f'{psutil.cpu_percent()} %', inline=False)
        embedInfo.add_field(name="Memory Usage", value=f'{psutil.virtual_memory().percent} %', inline=False)
        embedInfo.add_field(name="Latency", value=f'{ctx.bot.latency*1000:.2f} ms', inline=False)
        embedInfo.add_field(name="Database", value=db_info, inline=False)
        embedInfo.add_field(name="Database Pool", value=db_pool_info, inline=False)
        embedInfo.set_footer(text="End of bot info.")
        await ctx.send(embed=embedInfo)
        
    @commands.command(
        description=f"Let the bot guide you trough the initial setup",
        usage=f"$run_setup_helper",
    )
    async def run_setup_helper(self, ctx):
        timeout = 30.0
        message = ctx.message
        client = ctx.bot
        author = message.author.name
        channel = message.channel
        config={}
        config['guild'] = message.guild.id

        run = True
        while run:
            # At the moment only error we can use in this approach is asyncio.TimeoutError, so it's gonna be ugly for awhile.
            await message.channel.send(f"Enter the name of the category that will be used as part for the Feedback Channel.[1/8]")
            try:
                msg = await client.wait_for('message', timeout=timeout)
                config['category'] = msg.content
            except asyncio.TimeoutError:
                await exit_timeout(msg)
                break
    
            await message.channel.send(f"Enter the name of the channel that will be used for feedback.[2/8]")
            try:
                msg = await client.wait_for('message', timeout=timeout)
                config['channel'] = msg.content
            except asyncio.TimeoutError:
                await exit_timeout(msg)
                break

            await message.channel.send(f"Enter the minimum lenght for feedback to be considered valid.[3/8]")
            try:
                msg = await client.wait_for('message', timeout=timeout)
                config['min_lenght'] = msg.content
            except asyncio.TimeoutError:
                await exit_timeout(msg, is_numeric=True)
                break

            await message.channel.send(f"Enter the maximum number of feedback posts to consider request fulfiled.[4/4]")
            try:
                msg = await client.wait_for('message', timeout=timeout)
                config['max_feedback'] = msg.content
            except asyncio.TimeoutError:
                await exit_timeout(msg, is_numeric=True)
                break

def setup(bot):
    bot.add_cog(Admin(bot))