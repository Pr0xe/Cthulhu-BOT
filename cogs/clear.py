import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount:int):
        channel = ctx.message.channel
        if amount < 0:
            await ctx.send("Amount cannot be negative")
            print("ERROR: negative amount")
        elif amount > 100:
            embed=discord.Embed(title="User ERROR", description=f"{ctx.message.author.mention} Cannot delete more than `100 messages`", color=0xff00f6)
            await ctx.send(embed=embed)       
        else:
             with channel.typing():
                await channel.purge(limit=amount+1)
                embed=discord.Embed(title=":recycle: Deleted Messages :recycle:", description=f"{ctx.message.author.mention} deleted `{amount}` messages", color=0x32CD32)
                await ctx.send(embed=embed)
                print(f"{amount} Message deleted")
        
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} No permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Permission Dennied to clear messages")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="User ERROR", description=f"{ctx.message.author.mention} Please enter an amount", color=0xff00f6)
            await ctx.send(embed=embed)
            print("amount missing")
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title="User ERROR", description=f"{ctx.message.author.mention} Bad Syntax", color=0xff00f6)
            await ctx.send(embed=embed)
            print("bad syntax for clear") 
        elif isinstance(error, commands.CommandInvokeError):
            embed=discord.Embed(title="User ERROR", description=f"{ctx.message.author.mention} Cannot delete more than `100 messages` or `14 days old`", color=0xff00f6)
            await ctx.send(embed=embed)
            print(error)
            print("Cannot delete more than 100 messages or 14 days old")         
            
def setup(client):
    client.add_cog(Clear(client))
