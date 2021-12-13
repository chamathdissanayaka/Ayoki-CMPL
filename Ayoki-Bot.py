import discord
from discord import Guild
import inspect
import re
import ast
import os, asyncio
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import has_permissions
import json

def get_prefix(bot_obj, message: Context) -> str:
    try:
        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]
    except AttributeError:
        return '<'
    except KeyError:
        return '<'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def on_guild_remove(guild: Guild):

    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    try:
        prefixes.pop(str(guild.id))

        with open("prefixes.json", 'w') as f:
            json.dump(prefixes, f, indent=4)

    except KeyError:
        pass


@bot.command(aliases=["PREFIX", "Prefix", "pREFIX"])
@has_permissions(administrator=True)
async def prefix(ctx: Context, new_prefix: str):

    if ctx.guild is None:

        await ctx.reply("**You cannot change the prefix outside of a server!**")
        return

    if len(new_prefix) > 25:

        await ctx.reply("**Prefix cannot be longer than 25 characters!**")
        return

    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = new_prefix

    with open("prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=25)

    await ctx.send(f"**Prefix changed to {new_prefix}**")


@prefix.error
async def prefix_error(ctx: Context, error: Exception):

    if isinstance(error, commands.MissingRequiredArgument):

        await ctx.reply("**Incorrect usage!\n"
                        f"Example: {get_prefix(bot, ctx)}prefix .**")

    elif isinstance(error, commands.MissingPermissions):

        await ctx.reply("**You do not have the permission to change the server prefix!**")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="<help for 💞Cuddles"))
    print('cutee Ayoki online!!')

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

@bot.command()
async def ping(ctx):
    async with ctx.typing():
        await asyncio.sleep(0.1)
    if round(bot.latency * 1000) <= 50:
        embed = discord.Embed(
            title="PONG", description=f":ping_pong: My latency is **{round(bot.latency *1000)}** milliseconds!", color=discord.Color.yellow())
    elif round(bot.latency * 1000) <= 100:
        embed = discord.Embed(
            title="PONG", description=f":ping_pong: My latency is **{round(bot.latency *1000)}** milliseconds!", color=discord.Color.blue())
    elif round(bot.latency * 1000) <= 200:
        embed = discord.Embed(
            title="PONG", description=f":ping_pong: My latency is **{round(bot.latency *1000)}** milliseconds!", color=discord.Color.red())
    else:
        embed = discord.Embed(
            title="PONG", description=f":ping_pong: My latency is **{round(bot.latency *1000)}** milliseconds!", color=discord.Color.green())
        embed.set_thumbnail(
            url="https://i.pinimg.com/236x/51/63/94/5163941395dfb3f0ccf14ec98487bede.jpg")
    await ctx.send(embed=embed)

bot.run("OTEyODk5MDA2OTkxMDY1MTQ4.YZ2pdA.CAQPvXpNLmwmkBcMgyhg4td5K6I")