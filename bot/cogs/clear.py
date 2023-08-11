import discord
from discord.ext import commands
import constants

class Clear(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True, description="Delete messages equals to give amount")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount:int):
        log_channel = self.bot.get_channel(constants.LOG_CHANNEL)
        channel = ctx.channel
        if amount < 0:
            await ctx.send("Amount cannot be negative")
            print("ERROR: negative amount")
        elif amount > 100:
            embed=discord.Embed(title="ERROR", description="Cannot delete more than **100 messages**", color=0xff0000)
            await ctx.send(embed=embed)       
        else:
            await channel.purge(limit=amount+1)
            await log_channel.send(f"User: {ctx.author.mention} deleted {amount} messages from {channel.mention}")

        
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="No permission to use this command.", color=0xff0000)
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="ERROR", description="Please enter an amount", color=0xff0000)
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title="ERROR", description="Bad Syntax", color=0xff0000)
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Clear(bot))