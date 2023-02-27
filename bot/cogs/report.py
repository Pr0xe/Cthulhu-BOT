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
from discord import app_commands

nest_asyncio.apply()

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.run_until_complete(self.create_db_pool())

    @commands.Cog.listener()
    async def on_ready(self):
        await self.pg_con.execute("CREATE TABLE IF NOT EXISTS reports (user_id character varying, report TEXT[])")
        print(colored("Report system ready", 'green')) 

    async def create_db_pool(self):
        try:
            with open("data/pass.json") as password:
                PASS = json.load(password)
            self.pg_con = await asyncpg.create_pool(database="discordbot", user="pr0xe", password=PASS["password"])
            print(colored("Reports database opened successfully", 'cyan'))
        except:
            print(colored("Unable to connect", 'red'))

    @commands.hybrid_command(name="report", with_app_command=True ,description="Report user")
    @app_commands.guilds(constants.SERVER_ID)
    @app_commands.describe(member="Mention the member you want", reason="Provide the reason")
    async def report(self, ctx, member: discord.Member, *, reason:str):
        log_channel = self.bot.get_channel(constants.LOG_CHANNEL)
        warn_embed = discord.Embed(
        title=":warning: Report Submitted :warning:",
        colour=0xFF0000)
        warn_user = discord.Embed(
            colour=0x40E0D0,
            timestamp=ctx.message.created_at)
        if not reason:
            await ctx.reply("Please provide a reason!")
            return
        reason = ''.join(reason[:])
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
        warn_embed.add_field(name="Report Status", value=f"{ctx.message.author.mention} created a report for user : {member.mention}", inline=False)
        await log_channel.send(f"{ctx.message.author} reported the user {member.name}")
        warn_embed.add_field(name="Reason", value=reason, inline=False)
        await channel.send(embed=warn_embed)
        
    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description="Specify the user", color=0xff0000)
            await ctx.reply(embed=embed)
    
    @commands.hybrid_command(name="dreport", with_app_command=True ,description="Delete reports from user")
    @app_commands.guilds(constants.SERVER_ID)
    @app_commands.describe(member="Mention the member you want")
    @commands.has_permissions(ban_members=True)
    async def dreport(self, ctx, member:discord.Member):
        drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_heart:",
                colour=0xFFFFFF)
        member_id = str(member.id)
        user = await self.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
        if not user:
            drep_embed.add_field(name="Reports not found", value=f"{member} has clear record", inline=False)
            await ctx.send(embed=drep_embed)
            return
        else:
            drep_embed = discord.Embed(
                title=":white_circle: Report Status :white_heart:",
                colour=0xFFFFFF)
            member_id = str(member.id)
            await self.pg_con.execute("DELETE FROM reports WHERE user_id = $1", member_id)
            drep_embed.add_field(name="Reports Cleared", value=f"{ctx.message.author.mention} removed reports for user:  {member.name}", inline=False)
            await ctx.send(embed=drep_embed)
       
    @dreport.error
    async def dreport_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="You have no permission to use this command.", color=0xff0000)
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Missing User", description="Specify the user!", color=0xff0000)
            await ctx.reply(embed=embed)

    @commands.hybrid_command(name="reports", with_app_command=True ,description="Print report database or user report records")
    @app_commands.guilds(constants.SERVER_ID)
    @app_commands.describe(member="Mention the member you want")
    async def reports(self, ctx, member: discord.Member = None):
        drep_embed = discord.Embed(
                title=":man_judge:  Report History :man_judge:",
                colour=0xFF0000)
       
        if not member:
            if not ctx.message.author.guild_permissions.administrator:
                embed=discord.Embed(title="Permission Denied.", description="You can see only your's report history", color=0xff0000)
                return await ctx.send(embed=embed)
            else:
                data = await self.pg_con.fetch("SELECT * from reports ORDER BY array_length(report,1) DESC")    
                for i in range(len(data)):
                    drep_embed.add_field(name=f"{self.bot.get_user(int(data[i][0]))}", value=f"`reports : {len(data[i][1])}`", inline=False)
                await ctx.send(embed=drep_embed)
                return
        member_id = str(member.id)
        if member_id == str(ctx.author.id):
            user = await self.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
            if not user:
                drep_embed.add_field(name="Reports not found", value=f"{member.name} has clear record", inline=False)
                await ctx.send(embed=drep_embed)
                return
            else:
                rows = await self.pg_con.fetch("SELECT report FROM reports WHERE user_id = $1", member_id)
                data = await self.pg_con.fetch("SELECT * from reports ORDER BY array_length(report,1) DESC")    
                clean_rows = "\n".join(re.findall(r"'([^']+)'", str(rows)))

                for i in range(len(data)):
                    if (str(data[i][0]) == member_id):
                        rep_count = len(data[i][1])
                rep_embed = discord.Embed(
                    title=f"{member}",
                    description="User report history",
                    colour=0xFF0000)
                rep_embed.add_field(name=f"Report reasons - `{rep_count} Reports`", value=f"{str(clean_rows)}", inline=False)
                await ctx.send(embed=rep_embed)
                return
        elif ctx.message.author.guild_permissions.administrator:
            user = await self.pg_con.fetch("SELECT * FROM reports WHERE user_id = $1", member_id)
            if not user:
                drep_embed.add_field(name="Reports not found", value=f"{member.name} has clear record", inline=False)
                await ctx.send(embed=drep_embed)
                return
            else:
                rows = await self.pg_con.fetch("SELECT report FROM reports WHERE user_id = $1", member_id)
                data = await self.pg_con.fetch("SELECT * from reports ORDER BY array_length(report,1) DESC")    
                clean_rows = "\n".join(re.findall(r"'([^']+)'", str(rows)))

                for i in range(len(data)):
                    if (str(data[i][0]) == member_id):
                        rep_count = len(data[i][1])
                rep_embed = discord.Embed(
                    title=f"{member}",
                    description="User report history",
                    colour=0xFF0000)
                rep_embed.add_field(name=f"Report reasons - `{rep_count} Reports`", value=f"{str(clean_rows)}", inline=False)
                await ctx.send(embed=rep_embed)
                return
        else:
            embed=discord.Embed(title="Permission Denied.", description="You can't see reports of other users", color=0xff0000)
            return await ctx.send(embed=embed)
    
    @reports.error
    async def reports_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Missing User", description="Specify the user!", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="You have no permission to use this command.", color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Report(bot),guilds=[discord.Object(id=constants.SERVER_ID)])