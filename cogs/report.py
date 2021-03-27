import discord
import json
from discord.ext import commands
from discord import Embed, Member

with open('reports.json', "r", encoding='utf-8') as f:
            try:
                report = json.load(f)
            except ValueError:
                report = {}
                report['users'] = []

class Report(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context = True, aliases=['rep'])
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def report(self, ctx, user: discord.Member, *reason:str):
        warn_embed = discord.Embed(
        title=":warning: User Report :warning:",
        colour=0xFF0000)
        if not reason:
            await ctx.send(f"{ctx.message.author.mention} Please provide a reason!")
            return
        reason = ' '.join(reason) 
        for current_user in report['users']:
            if current_user['name'] == user.name:
                current_user['reasons'].append(reason)
                break
        else:
            report['users'].append({
                'name':user.name,
                'reasons': [reason,]
            })
        with open('reports.json','w+') as f:
            json.dump(report, f, indent=4)
            
        warn_embed.add_field(name="Report Committed", value=f"{ctx.message.author.mention} reported the user {user.mention}", inline=False)
        warn_embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=warn_embed)
        print("report committed")
    
    @commands.command(pass_context = True)
    async def reports(self, ctx, user:discord.Member):
        for current_user in report['users']:
            if user.name == current_user['name']:
                total = len(current_user['reasons'])
                if total != 0:
                    await ctx.send(f"**{user.mention}** has been reported {total} times")
                    break
                else:
                    await ctx.send(f"**{user.name}** has never been reported")
    
    @commands.command(pass_context = True, aliases=['drep'])
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def dreport(self, ctx, user:discord.Member):
        for current_user in report['users']:
            if current_user['name'] == user.name:
                if len(current_user['reasons']) == 0:
                    await ctx.send(f"{ctx.message.author.mention} Reports not found")
                    break
                else:
                    while current_user['reasons']:
                        current_user['reasons'].pop()
                    embed=discord.Embed(title=" :white_check_mark: Reports Deleted :white_check_mark: ", description=f"{ctx.message.author.mention} Removed all reports from {user.mention}", color=0x00b3ad)
                    await ctx.send(embed=embed)
                    print(f"remove report from user:{user.name}")
                    break
        with open('reports.json','w+') as f:
            json.dump(report, f, indent=4)
       
    @dreport.error
    async def dreport_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} You have no permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Permission Dennied to remove Report")

    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description=f"{ctx.message.author.mention} You have no permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Permission Dennied to Report")

        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Arguments Missing", description=f"Specify the user", color=0xff00f6)
            await ctx.send(embed=embed)
            print("Argument missing for reports")


def setup(client):
    client.add_cog(Report(client))                
