import discord
import asyncio, datetime
from discord.ext import commands

class Server_Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=':Get the information about this server \n:Do <serverinfo')
    async def serverinfo(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(0.1)
        embed = discord.Embed(title=f"{ctx.guild.name}", description="Server Information",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="Server created at",
                    value=f"{ctx.guild.created_at}")
        embed.add_field(name="Server Owner",
                    value=f"{ctx.guild.owner.display_name}")
        embed.add_field(name="Server Region", value=f"{ctx.guild.region}", inline=False)
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        embed.set_footer(
        text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        # embed.set_thumbnail(url=f"{ctx.guild.icon}")
        embed.set_thumbnail(
        url="https://img.icons8.com/nolan/2x/server.png")
        embed.set_image(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Server_Information(bot))