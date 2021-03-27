import discord
from discord.ext import commands
from discord import Embed, Member

class Unmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        await member.edit(mute=False)
        embed=discord.Embed(title=" :sound: User Unmuted! :sound:", description="**{0}** is now Unmuted!".format(member.mention), color=0xff00f6)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.send(f"You are voice unmuted at {ctx.guild.name} Server. Reason:`{reason}`")

    
    @unmute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
            await ctx.say(embed=embed)

def setup(client):
    client.add_cog(Unmute(client))