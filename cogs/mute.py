import discord
from discord.ext import commands
from discord import Embed, Member

class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True)
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        await member.edit(mute=True)
        embed=discord.Embed(title=" :mute: User Muted! :mute: ", description="**{0}** is mute by **{1}**!".format(member.mention, ctx.message.author.mention), color=0xff00f6)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
        em2u=discord.Embed(title=":mute: Server Muted :mute:", description="You are muted by **{0}**!".format(ctx.message.author.mention), color=0xff0000)
        em2u.add_field(name="Reason", value=reason, inline=False)
        await member.send(embed=em2u)
    
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
            await ctx.say(embed=embed)

def setup(client):
    client.add_cog(Mute(client))