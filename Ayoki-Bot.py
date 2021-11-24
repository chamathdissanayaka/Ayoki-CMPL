import discord
import inspect
import re
import ast
import os
from discord.ext import commands


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='<', intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="<help for Cuddles💞"))
    print('cutee Ayoki online!!')

for filename in os.listdir('C:/Users/Chamath/Documents/GitHub/Ayoki-CMPL/cogs'):
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


bot.run('token')
