import discord
from discord.ext import commands
from discord import Embed, Member
import constants
from discord import app_commands

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="mute", with_app_command=True ,description="Mute a user")
    @app_commands.guilds(constants.SERVER_ID)
    @app_commands.describe(member="Add member", reason="Provide a reason for mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        log_channel = self.bot.get_channel(constants.LOG_CHANNEL)
        await member.edit(mute=True)
        embed=discord.Embed(title=" :mute: User Muted! :mute: ", description="**{0}** is  server muted by **{1}**!".format(member.mention, ctx.message.author.mention), color=0xff00f6)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
        await log_channel.send(f"user : {member} is voice muted by {ctx.author}")
  
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command", color=0xff0000)
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description="Specify the user", color=0xff0000)
            await ctx.reply(embed=embed)
            
    @commands.hybrid_command(name="unmute", with_app_command=True ,description="Unmute a user")
    @app_commands.guilds(constants.SERVER_ID)
    @app_commands.describe(member="Add member")
    async def unmute(self, ctx, member: discord.Member):
        log_channel = self.bot.get_channel(constants.LOG_CHANNEL)
        await member.edit(mute=False)
        embed=discord.Embed(title=" :sound: User Unmuted! :sound:", description="**{0}** is Server Unmuted!".format(member.mention), color=0xff00f6)
        await ctx.send(embed=embed)
        await log_channel.send(f"user : {member} is now unmuted by {ctx.author}")
    
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command", color=0xff0000)
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description="Specify the user", color=0xff0000)
            await ctx.reply(embed=embed)
            
async def setup(bot):
    await bot.add_cog(Mute(bot),guilds=[discord.Object(id=constants.SERVER_ID)])