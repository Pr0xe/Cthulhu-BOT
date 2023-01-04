from array import array
import discord
import asyncpg
import asyncio
import nest_asyncio
import json
from discord import embeds
from discord.ext import commands
from discord import Embed, Member
from discord.ext.commands.errors import MissingRequiredArgument
from termcolor import colored
import re
import constants

nest_asyncio.apply()

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.run_until_complete(self.create_db_pool())

    @commands.Cog.listener()
    async def on_ready(self):
        await self.pg_con.execute("CREATE TABLE IF NOT EXISTS reports (user_id character varying, report TEXT[])")
        print("report system ready") 

    async def create_db_pool(self):
        try:
            with open("data/pass.json") as password:
                PASS = json.load(password)
            self.pg_con = await asyncpg.create_pool(database="discordbot", user="pr0xe", password=PASS["password"])
            print(colored("Reports database opened successfully", 'cyan'))
        except:
            print(colored("Unable to connect", 'red'))

    @commands.command(pass_context = True, aliases=['rep'])
    async def report(self, ctx, member: discord.Member, *reason:str):
        log_channel = self.bot.get_channel(constants.LOG_CHANNEL)
        warn_embed = discord.Embed(
        title=":warning: Report Submitted :warning:",
        colour=0xFF0000)
        warn_user = discord.Embed(
            colour=0x40E0D0,
            timestamp=ctx.message.created_at)
        if not reason:
            await ctx.send(f"{ctx.message.author.mention} Please provide a reason!")
            return
        reason = ' '.join(reason)
        member_id = str(member.id)

        user = await self.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)

        if not user:
            await self.pg_con.execute("INSERT INTO reports (user_id, report) VALUES($1, ARRAY[$2])", member_id, reason)
            warn_user.add_field(name=":white_check_mark: Report Submitted :white_check_mark:", value=f"Thank for your report!", inline=False)
            warn_user.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=warn_user)
        else:
            await self.pg_con.execute("UPDATE reports SET report = array_append(report, $1) WHERE user_id = $2", reason, member_id)
            warn_user.add_field(name=":white_check_mark: Report Submitted :white_check_mark:", value=f"Thank for your report!", inline=False)
            warn_user.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=warn_user)
        
        channel = self.bot.get_channel(constants.REPORT_CHANNEL)
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
        user = await self.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
        if not user:
            drep_embed.add_field(name="Reports not found", value=f"{member.mention} Seems to be clear!", inline=False)
            await ctx.send(embed=drep_embed)
            return
        else:
            drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_heart:",
                colour=0xFFFFFF)
            member_id = str(member.id)
            await self.pg_con.execute("DELETE FROM reports WHERE user_id = $1", member_id)
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
    async def reports(self, ctx, member: discord.Member = None):
        drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_circle:",
                colour=0xFFFFFF)
        if not member:
            users_id = await self.pg_con.fetch("SELECT user_id FROM reports")
            IDS = re.findall('[0-9]+', str(users_id))
            if not IDS:
                drep_embed.add_field(name="Reports not found", value="0", inline=False)
                await ctx.send(embed=drep_embed)
                return
            for i in range(len(IDS)):
                array_len = await self.pg_con.fetch("SELECT array_length(report,1) FROM reports WHERE user_id = $1", IDS[i])
                temp_string = str(array_len)
                total_reports = ''.join(filter (lambda i: i.isdigit(), temp_string))
                user = self.bot.get_user(int(IDS[i]))
                drep_embed.add_field(name=f"{user}", value=f"**{str(total_reports)}** reports in history", inline=False)    
            await ctx.send(embed=drep_embed)
            return
        member_id = str(member.id)
        user = await self.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
        if not user:
            drep_embed.add_field(name="Reports not found", value=f"{member.mention} Seems to be clear!", inline=False)
            await ctx.send(embed=drep_embed)
            return
        else:
            rows = await self.pg_con.fetch("SELECT report FROM reports WHERE user_id = $1", member_id)
            clean_rows = re.findall(r"'([^']+)'", str(rows))
            rep_embed = discord.Embed(
                title=f"User report history - {member}",
                colour=0xFFFFFF)
            rep_embed.add_field(name="Report messages", value=f"{str(clean_rows)}", inline=False)
            await ctx.send(embed=rep_embed)
            return
    
    @reports.error
    async def reports_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Missing User", description=f"{ctx.message.author.mention} Specify the user!", color=0xff00f6)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} You have no permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Report(bot))