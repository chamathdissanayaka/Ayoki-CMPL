from discord.ext.commands.context import Context
from discord.ext.commands import has_permissions
from discord.ext import commands
import os, asyncio, json, re, ast, inspect, aiohttp
from discord import Guild, utils
import discord
from urllib import parse
from typing import List

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

def get_prefix(bot_obj, message: Context) -> str:
    try:
        with open("bot/prefixes.json", 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]
    except AttributeError:
        return '!'
    except KeyError:
        return '!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

for filename in os.listdir("./cogs"):  
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="<help for 💞Cuddles"))
    print(f"{bot.user} is Online!!")

@bot.event
async def on_guild_remove(guild: Guild):
    with open("bot/prefixes.json", 'r') as f:
        prefixes = json.load(f)
    try:
        prefixes.pop(str(guild.id))
        with open("bot/prefixes.json", 'w') as f:
            json.dump(prefixes, f, indent=4)
    except KeyError:
        pass

@bot.command(aliases=["PREFIX", "Prefix", "pREFIX"])
@has_permissions(administrator=True)
async def setprefixto(ctx: Context, new_prefix: str):
    if ctx.guild is None:
        await ctx.reply("**You cannot change the prefix outside of a server!**")
        return
    if len(new_prefix) > 25:
        await ctx.reply("**Prefix cannot be longer than 4 characters!**")
        return
    with open("bot/prefixes.json", 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = new_prefix
    with open("bot/prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent=25)
    await ctx.send(f"**Prefix changed to {new_prefix}**")

@setprefixto.error
async def prefix_error(ctx: Context, error: Exception):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("**Incorrect usage!\n"
                        f"Example: {get_prefix(bot, ctx)}prefix `Your_new_Prefix`**")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("**You do not have the permission to change the server prefix!**")

snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

@bot.event
async def on_message_delete(message):

    global snipe_message_content
    global snipe_message_author
    global snipe_message_id

    snipe_message_content = message.content
    snipe_message_author = message.author.id
    snipe_message_id = message.id
    await asyncio.sleep(60)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None


@bot.command(help='shows the last delted message of any user')
async def snipe(message):
    if snipe_message_content == None:
        await message.channel.send("Theres nothing to snipe.")
    else:
        embed = discord.Embed(title='Message Deleted at Last',
                              description=f"`deleted`: {snipe_message_content}")
        embed.set_thumbnail(
            url='https://c4.wallpaperflare.com/wallpaper/295/469/168/anime-anime-girls-gun-weapon-wallpaper-preview.jpg')
        embed.set_footer(
            text=f"Requested by by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar.url)
        embed.add_field(name='Done By', value=f'<@{snipe_message_author}>')
        await message.channel.send(embed=embed)
        return

@bot.event
async def on_member_join(member: discord.Member):
  order = sorted(member.guild.members, key=lambda member: member.joined_at or discord.utils.utcnow()).index(member) + 1
  channel = member.guild.system_channel
  if not channel: # There is no welcome channel
    channel = discord.utils.find(lambda chan: "general" in chan.name.lower(), member.guild.text_channels, channel=922451779210346511) # find a channel that has 'general' in it.
    if not channel:
      channel = discord.utils.find(lambda chan: chan.permissions_for(member.guild.me).send_messages, member.guild.text_channels)
      
  bg_url = "https://cdn.discordapp.com/attachments/850808002545319957/859359637106065408/bg.png"
  text_1 = parse.quote(f"Welcome to {member.guild.name}")
  text_2 = f"{member.name}"
  text_3 = parse.quote(f"You are #{order} member of the Server")
  await channel.send(f"https://api.popcat.xyz/welcomecard?background={bg_url}&text1={text_1}&text2={text_2}&text3={text_3}&avatar={member.avatar.url}")

WIKI_ENDPOINT = 'https://en.wikipedia.org/w/api.php'
NUMBER_OF_SENTENCES = 3

@bot.command(help='Search on Wikipedia')
async def wiki(ctx, *query_elements):
    async with ctx.typing():
        await asyncio.sleep(1)
    query = ' '.join(query_elements)
    params = {
        "action": "query",
        "prop": "extracts",
        "titles": query,
        "exsentences": NUMBER_OF_SENTENCES,
        "explaintext": "true",
        "format": "json",
        "redirects": "true"
    }
    headers = {"User-Agent": "BOT-NAME_CHANGE-ME/1.0"}

    async with aiohttp.ClientSession() as session:
        async with session.get(WIKI_ENDPOINT, params=params, headers=headers) as r:
            data = await r.json()
            pages = data['query']['pages']
            page = pages[list(pages)[0]]
            try:
                extract = page['extract']
                if extract is None:
                    raise ValueError
            except:
                extract = f"We could not fetch an extract for this page. Perhaps it does not exist, or the wiki queried does not support the **TextExtracts** MediaWiki extension: https://www.mediawiki.org/wiki/Extension:TextExtracts\nThe page data received is: `{page}`"
            await ctx.send(extract)

bot.run('OTEyODk5MDA2OTkxMDY1MTQ4.YZ2pdA.CAQPvXpNLmwmkBcMgyhg4td5K6I')
