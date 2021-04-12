import discord
from discord.ext import commands
from discord import Embed, Member

class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        await member.edit(mute=True)
        embed=discord.Embed(title=" :mute: User Muted! :mute: ", description="**{0}** is mute by **{1}**!".format(member.mention, ctx.message.author.mention), color=0xff00f6)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
        print(f"user : {member} is voice muted by {ctx.author}")
  
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="{0} You don't have permission to use this command".format(ctx.author.mention), color=0xff00f6)
            await ctx.send(embed=embed)
            print(f"Permission denied to {ctx.author}")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description="{0} Specify the user".format(ctx.author.mention), color=0xff00f6)
            await ctx.send(embed=embed)
            print(f"Not specified user by: {ctx.author}")
            
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        await member.edit(mute=False)
        embed=discord.Embed(title=" :sound: User Unmuted! :sound:", description="**{0}** is now Unmuted!".format(member.mention), color=0xff00f6)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
        print(f"user : {member} is now unmuted by {ctx.author}")
    
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="{0} You don't have permission to use this command".format(ctx.author.mention), color=0xff00f6)
            await ctx.send(embed=embed)
            print(f"Permission denied to {ctx.author}")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description="{0} Specify the user".format(ctx.author.mention), color=0xff00f6)
            await ctx.send(embed=embed)
            print(f"Not specified user by: {ctx.author}")
def setup(client):
    client.add_cog(Mute(client))