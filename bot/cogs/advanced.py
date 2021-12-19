import discord
import json
from discord.ext import commands
from discord import Embed, Member

class Advanced(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(pass_context = True)
    @commands.has_permissions(kick_members=True)
    async def advanced(self, ctx):
        with open("data/prefixes.json", 'r') as f:
                prefixes = json.load(f)    
        pre = prefixes[str(ctx.guild.id)]
        embed_mod = discord.Embed(
            colour = 0xFF0000,
            title = "Server Moderation",
            description = ":no_entry: **Commands for Admins & Moderators** :no_entry: ",
        )
        fields_mod = [
            ("Prefix for this server", f"prefix: `{pre}`", False),
            ("```cprefix <prefix>```", 'Change the prefix :no_entry: Admins ONLY :no_entry:', False),
            ("```clear <amount>```", 'Clear the amount of messages you want', False),
            ("```ban <@member> <reason>```", 'BAN user from the server', False),
            ("```kick <@member> <reason>```", 'Kick user from the server', False),
            ("```unban <username#number> <reason>```", 'Unban user to join again the server', False),
            ("```mute <@member> <reason>```", 'Server voice mute a user', False),
            ("```unmute <@member> <reason>```", 'Voice unmute the user', False),
            ("```rmlevel <@member>```", 'Remove level from user', False),
            ("```role <@role> <@member>```", 'Add role to a member', False),
            ("```rmrole <@role> <@member>```", 'Remove role from member', False),
            ("```crole <rolename> ```", 'Create new role in Server', False),
            ("```drole <rolename> ```", 'Delete role from Server', False),
            ("```report <@member> <reason>```", 'Report user for a serious reason', False),
            ("```reports <@member>```", 'Report history for the user', False),
            ("```dreport <@member>```", 'Remove reports from the user', False),
            ("```messages```", 'List deleted messages', False),
            ("```dmessages```", 'Remove deleted messages', False),
            (":underage: ```nsfw or nsfw <subreddit>``` :underage: ", 'NSFW content from reddit, **default sub is nsfw**', False),
        ]
        for name, value, inline in fields_mod:
            embed_mod.add_field(name=name, value=value, inline=inline)
        log_channel = self.bot.get_channel(900492686581178398)
        embed_mod.set_footer(text="Contact with Administrators for more help")
        await ctx.send(embed=embed_mod)
        await log_channel.send(f"Advanced commands printed : requested by {ctx.author}")
        
    @advanced.error
    async def advanced_error(self, ctx ,error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} No permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Advanced(bot))