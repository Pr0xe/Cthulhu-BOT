import discord
from discord.ext import commands
from discord import Embed, Member

class BanKick(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context = True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(
        title="User Status",
        colour=0xFF0000)
        await member.ban(reason=reason)
        embed.add_field(name=" :hammer: User Banned :hammer: ", value=f"{ctx.message.author.mention} banned {member.mention} from the Server", inline=True)
        embed.add_field(name="Reason", value=reason , inline=False)
        await ctx.send(embed=embed)
        print("BAN {} DONE".format(member))

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="{ctx.message.author.mention} No permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Permission Dennied to ban")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description=f"Specify the user", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Argument missing for ban")

    @commands.command(pass_context = True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} Unbanned ')
                return
                
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="{ctx.message.author.mention} You have no permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Permission Dennied to unban")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description=f"Specify the user", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Argument missing for kick")


    @commands.command(pass_context = True, name ='kick')
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        embed = discord.Embed(
        title="User Status",
        colour=0xFFF200)
        await user.kick(reason=reason)
        embed.add_field(name=" :punch: User Kicked :punch:", value=f"{ctx.message.author.mention} kicked {user.mention} from the Server", inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
        print("kicked {} DONE".format(user))
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} You have no permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Permission Dennied to kick")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description=f"Specify the user", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Argument missing for kick")

def setup(client):
    client.add_cog(BanKick(client))            