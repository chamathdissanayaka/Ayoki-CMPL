import discord
from discord.ext import commands
import subprocess
import time
import os


class Compile(commands.Cog):

    def __init__(self, client):
        self.client = client

    # --------------commands
    @commands.command(help='compiles python program.')
    async def eval(self, ctx, *, arg):
        """
        : Do <`code here`
        """

        start = time.process_time()
        arg = arg[6:]
        arg = arg.split("```")
        param = arg[1]
        f = open("in.txt", "w")
        f.write(param)
        f.close()
        # arg="try:"+arg[0].replace('\n','\n\t')+"\nexcept:\n\tprint(\"Error\")"
        arg = arg[0]
        f = open("exec.py", "w")
        f.write(arg)
        f.close()
        try:
            res = subprocess.check_output(
                "python exec.py < in.txt", shell=True)
        except:
            res = "Error".encode("utf-8")
        tot_time = str(time.process_time() - start)
        os.remove("in.txt")
        os.remove("exec.py")
        embed = discord.Embed(
            title='compilation results',
            color=discord.Color.blurple()
        )
        if res != "Error".encode("utf-8"):
            embed.add_field(
                name="Status", value='```ruby\nFinished with exit code: 0```', inline=False)
            embed.add_field(name="program output", value='```python\n' +
                            res.decode("utf-8")+'```', inline=False)
        else:
            embed.add_field(
                name="Status", value='```ruby\nError```', inline=False)
        embed.add_field(name='Total Time taken is : ',
                        value=f'```css\n {tot_time}```', inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Compile(bot))
