import discord
import DiscordUtils
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    music = DiscordUtils.Music()

    @commands.command(aliases=['j','J','JOIN','Join','connect','CONNECT','Connect'])
    async def join(self,ctx):
        await ctx.author.voice.channel.connect()
        await ctx.reply('Voice Connected')
        
    @commands.command(aliases=['Leave','LEAVE','DC','dc','Dc','Disconnect','fuckoff', 'get the fuck out','bye','Bye','api kapemu','disconnect','bye bitch'])
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.reply('Disconnected from VC')

def setup(bot):
    bot.add_cog(Music(bot)) 
