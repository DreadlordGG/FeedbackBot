from discord.ext import commands
from core.logging import getLogger
logger = getLogger(__name__)
from core.models import Server, Posts, Users
from sqlalchemy.future import select
from urllib.parse import urlparse
from sqlalchemy.dialects.postgresql import insert

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description=f"Posts a feedback request people can comment on. You must have at least one point to post a track for feedback.",
        usage=f"",
    )    

    async def post(self, ctx):
        allowed_links = []
        async with ctx.bot.engine.connect() as conn:
            stmt = (
                select(Server)
            )
            result = await conn.execute(stmt)
            allowed_links = result.fetchone()._asdict()['allowed_links']
        link, body = ctx.message.content.split(" ",2)[1:]
        link = urlparse(link)
        if link.scheme:
            if link.netloc in allowed_links:
                async with self.bot.engine.connect() as conn:
                    stmt = (
                        insert(Users).
                        values(userid=ctx.message.author.id, guild=ctx.guild.id                      
                        ).on_conflict_do_nothing()
                    )          
                    await conn.execute(stmt)       

                    stmt = (
                        insert(Posts).
                        values(userid=ctx.message.author.id, link=link.geturl(), body=body, guild=ctx.guild.id                      
                        )
                    )            
                    result = await conn.execute(stmt)    
                await ctx.message.add_reaction("✅")
            else:
                await ctx.message.delete()
                await ctx.message.channel.send(f"{ctx.message.author.mention} The link source used in your request is not allowed in this server. Allowed sources are {','.join(allowed_links)}")                
        else:
            await ctx.message.delete()
            await ctx.message.channel.send(f"{ctx.message.author.mention} The link needs to start with http or https")

    @commands.command(
        description=f"Submits a feedback for the track with the given request ID. If your feedback is acceptable you will receive a point.",
        usage=f"",
    )    

    async def feedback(self, ctx):
        pass
    @commands.command(
        description=f"Shows tracks requesting feedback that have not recieved any",
        usage=f"",
    )    

    async def need(self, ctx):
        pass
    @commands.command(
        description=f"DMs all the feedback given for requests containing the given link.",
        usage=f"",
    )    
    
    async def getFeedback(self, ctx):
        pass
def setup(bot):
    bot.add_cog(User(bot))