import discord
import asyncio
from discord.ext import commands
from discord import Embed, Member

class Report(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context = True, aliases=['rep'])
    async def report(self, ctx, member: discord.Member, *reason:str):
        log_channel = self.client.get_channel(900492686581178398)
        warn_embed = discord.Embed(
        title=":warning: Report Submitted :warning:",
        colour=0xFF0000)
        warn_user = discord.Embed(
            colour=0x40E0D0)
        if not reason:
            await ctx.send(f"{ctx.message.author.mention} Please provide a reason!")
            return
        reason = ' '.join(reason)
        member_id = str(member.id)
        user = await self.client.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
        if not user:
            await self.client.pg_con.execute("INSERT INTO reports (user_id, report) VALUES($1, ARRAY[$2])", member_id, reason)
            warn_user.add_field(name=":white_check_mark: Report Submitted :white_check_mark:", value=f"Thank for your report!", inline=False)
            warn_user.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=warn_user)
        else:
            await self.client.pg_con.execute("UPDATE reports SET report = array_append(report, $1) WHERE user_id = $2", reason, member_id)
            warn_user.add_field(name=":white_check_mark: Report Submitted :white_check_mark:", value=f"Thank for your report!", inline=False)
            warn_user.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=warn_user)
        
        channel = self.client.get_channel(802344348825157632)
        warn_embed.add_field(name="Report Status", value=f"{ctx.message.author.mention} reported the user {member.mention}", inline=False)
        await log_channel.send(f"{ctx.message.author.mention} reported the user {member.mention}")
        warn_embed.add_field(name="Reason", value=reason, inline=False)
        await channel.send(embed=warn_embed)
        
    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description=f"{ctx.message.author.mention} Specify the user", color=0xff00f6)
            await ctx.send(embed=embed)
    
    @commands.command(pass_context = True, aliases=['drep'])
    @commands.has_permissions(kick_members=True)
    async def dreport(self, ctx, member:discord.Member):
        drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_heart:",
                colour=0xFFFFFF)
        member_id = str(member.id)
        user = await self.client.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
        if not user:
            drep_embed.add_field(name="Reports not found", value=f"{member.mention} Seems to be clear!", inline=False)
            await ctx.send(embed=drep_embed)
            return
        else:
            drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_heart:",
                colour=0xFFFFFF)
            member_id = str(member.id)
            await self.client.pg_con.execute("DELETE FROM reports WHERE user_id = $1", member_id)
            drep_embed.add_field(name="Reports Cleared", value=f"{ctx.message.author.mention} removed reports from {member.mention}", inline=False)
            await ctx.send(embed=drep_embed)
       
    @dreport.error
    async def dreport_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} You have no permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Missing User", description=f"{ctx.message.author.mention} Specify the user!", color=0xff00f6)
            await ctx.send(embed=embed)

    @commands.command(pass_context = True)
    @commands.has_permissions(ban_members=True)
    async def reports(self, ctx, member: discord.Member):
        drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_heart:",
                colour=0xFFFFFF)
        member_id = str(member.id)
        user = await self.client.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
        if not user:
            drep_embed.add_field(name="Reports not found", value=f"{member.mention} Seems to be clear!", inline=False)
            await ctx.send(embed=drep_embed)
            return
        else:
            #array_len = await self.client.pg_con.fetch("SELECT array(length(report, 1) FROM reports WHERE user_id = $1", member_id)
            rows = await self.client.pg_con.fetch("SELECT report FROM reports WHERE user_id = $1", member_id)
            new_list=[]
            new_list.append(rows)
            drep_embed.add_field(name="Reports History", value=f"{new_list}", inline=False)
            await ctx.send(embed=drep_embed)
            return
    
    @reports.error
    async def reports_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Missing User", description=f"{ctx.message.author.mention} Specify the user!", color=0xff00f6)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Report(client))                
