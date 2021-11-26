import discord
import json, aiohttp, random, asyncio
from discord.ext import commands

class Giphy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, help='send Gifs')
    async def gif(self, ctx, *, search):
        async with ctx.typing():
            await asyncio.sleep(0.1)
        embed = discord.Embed(colour=discord.Colour.magenta())
        session = aiohttp.ClientSession()

        if search == '':
            response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=vBFb7XWFdnbCNn3Atf9FBbQ68XG4EoV9')
            data = json.loads(await response.text())
            embed.set_image(url=data['data']['images']['original']['url'])
        else:
            search.replace(' ', '+')
            response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=vBFb7XWFdnbCNn3Atf9FBbQ68XG4EoV9&limit=10')
            data = json.loads(await response.text())
            gif_choice = random.randint(0, 9)
            embed.set_image(url=data['data'][gif_choice]
                        ['images']['original']['url'])

        await session.close()

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Giphy(bot))