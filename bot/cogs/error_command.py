from discord.ext import commands

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f"{ctx.message.author.mention} Command not found")
        except:
            pass

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))