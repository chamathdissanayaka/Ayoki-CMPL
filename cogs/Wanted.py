import discord
import asyncio
from discord.ext import commands

class Wanted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wanted(self, ctx, *, member: discord.Member = None):
        async with ctx.typing():
            await asyncio.sleep(0.1)
            if not member:
                member=ctx.message.author
            await ctx.send(f"https://api.popcat.xyz/wanted?image={member.avatar.url}")             

def setup(bot):
    bot.add_cog(Wanted(bot))        