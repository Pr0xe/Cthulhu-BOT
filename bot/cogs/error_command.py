from discord.ext import commands

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if isinstance(error, commands.CommandNotFound):
                await ctx.reply(f"{ctx.message.author.mention} Command not found")
        except:
            pass

async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))