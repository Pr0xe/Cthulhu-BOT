import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test(self,ctx):
        await ctx.reply(f'**Cthulhu is Online :green_circle: ** \n_Made by <@188771015751368704>_')

async def setup(bot):
    await bot.add_cog(Test(bot))