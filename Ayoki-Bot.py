import discord
import inspect
import re
import ast
import os
import json

from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='<', intents=intents)


@bot.event
async def on_ready():
    print("cute Ayoki online!!")


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


bot.run(token)
