import discord
import asyncio
from discord.ext import commands

class Latency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(0.1)
        if round(self.bot.latency * 1000) <= 50:
            embed = discord.Embed(
                title="PONG", description=f":ping_pong: My latency is **{round(self.bot.latency *1000)}** milliseconds!", color=discord.Color.yellow())
        elif round(self.bot.latency * 1000) <= 100:
            embed = discord.Embed(
                title="PONG", description=f":ping_pong: My latency is **{round(self.bot.latency *1000)}** milliseconds!", color=discord.Color.blue())
        elif round(self.bot.latency * 1000) <= 200:
            embed = discord.Embed(
                title="PONG", description=f":ping_pong: My latency is **{round(self.bot.latency *1000)}** milliseconds!", color=discord.Color.red())
        else:
            embed = discord.Embed(
                title="PONG", description=f":ping_pong: My latency is **{round(self.bot.latency *1000)}** milliseconds!", color=discord.Color.green())
            embed.set_thumbnail(
                url="https://i.pinimg.com/236x/51/63/94/5163941395dfb3f0ccf14ec98487bede.jpg")
        await ctx.send(embed=embed)    

def setup(bot):
    bot.add_cog(Latency(bot))        