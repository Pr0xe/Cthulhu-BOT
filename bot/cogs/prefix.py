import os
import discord
import json
from discord.ext import commands
from discord import Embed, Member
from os.path import dirname, abspath

path = os.getcwd() 
final_path = os.path.join(path,'data','prefixes.json')

class Prefix(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles=True)
    async def cprefix(self,ctx,prefix):
        embed = discord.Embed(
        title="Server Status",
        colour=0xFFF200)
        with open(final_path,'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open(final_path,'w') as f:
            json.dump(prefixes, f, indent=4)
        embed.add_field(name="Prefix Changed", value=f"New prefix is `{prefix}`", inline=True)
        await ctx.send(embed=embed)
        print("prefix change to {}".format(prefix))
    
    @cprefix.error
    async def prefix_error(self, ctx ,error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} No permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Permission Dennied to change prefix")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="User ERROR", description=f"{ctx.message.author.mention} Prefix argument is missing", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Prefix missing")
        
async def setup(bot):
    await bot.add_cog(Prefix(bot))