import discord
import inspect
import re
import ast
import os, aiohttp, random, asyncio, json
from discord.ext import commands


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='<', intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="<help for Cuddles💞"))
    print('cutee Ayoki online!!')
@bot.command(pass_context=True, help='send Gifs', categories=': DO `<` `gif name`')
async def gif(ctx, *, search):
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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)


source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(
    r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',
    r"\1Discord Android\2",
    source_
)
loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"),
     discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]


bot.run("OTEyODk5MDA2OTkxMDY1MTQ4.YZ2pdA.CAQPvXpNLmwmkBcMgyhg4td5K6I")
