import discord
from discord.ext import commands
import platform

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, name="test")
    async def test(self,ctx):
        python_p = ["Python", platform.python_version()]
        await ctx.reply(f'**Cthulhu is Online** \n_Made by <@188771015751368704>_')

def setup(bot):
    bot.add_cog(Test(bot))