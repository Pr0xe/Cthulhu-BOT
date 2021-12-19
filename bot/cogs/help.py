import discord
import json
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(invoke_without_command = True)
    async def help(self, ctx):
        with open("data/prefixes.json", 'r') as f:
                prefixes = json.load(f)    
        pre = prefixes[str(ctx.guild.id)]
        embed_commands = discord.Embed(
            colour = 0x00FF00,
            title = "Commands",
            description = f"Use `{pre}`help <command> for extended information on a command"
        )
        embed_commands.add_field(name="Moderation - :no_entry: Only for Admins and Owner :no_entry:", value="`cprefix`, `clear`, `ban`, `unban`, `kick`, `mute`, `unmute`, `role`, `rmrole`, `crole`, `drole`, `dmessages`, `dreport`, `rmlevel`", inline= False) 
        embed_commands.add_field(name="Community", value="`who`, `server`, `bot`, `messages`, `poll`, `memes`, `level`, `nsfw(+18)`", inline= False)
        embed_commands.add_field(name="Reporting System", value="`report`, `reports`", inline= False)
        
        await ctx.send(embed=embed_commands)
        
    @help.command()
    async def kick(self, ctx):
        embed_commands = discord.Embed(title="Kick", description= "Kick user from the server", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">kick <member> [reason]")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def ban(self, ctx):
        embed_commands = discord.Embed(title="Ban", description= "Ban user from the server", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">ban <member> [reason]")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def unban(self, ctx):
        embed_commands = discord.Embed(title="Unban", description= "Unban user", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">unban <username#number> <reason> [reason]")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def cprefix(self, ctx):
        embed_commands = discord.Embed(title="Prefix", description= "Change the prefix :no_entry: Admins ONLY :no_entry:", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">cprefix <prefix>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def clear(self, ctx):
        embed_commands = discord.Embed(title="Clear", description= "Clear the amount of messages you want", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">clear <amount>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def mute(self, ctx):
        embed_commands = discord.Embed(title="Mute", description= "Server voice-mute user", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">mute <@member> <reason>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def unmute(self, ctx):
        embed_commands = discord.Embed(title="Unmute", description= "Voice unmute", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">unmute <@member> <reason>")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def level(self, ctx):
        embed_commands = discord.Embed(title="Level", description= "Check out your level in server", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">level")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def rmlevel(self, ctx):
        embed_commands = discord.Embed(title="rmlevel", description= "Remove level from user", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">rmlevel <@member>")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def role(self, ctx):
        embed_commands = discord.Embed(title="Role", description= "Add role to a member", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">role <@role> <@member>")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def rmrole(self, ctx):
        embed_commands = discord.Embed(title="rmrole", description= "Remove role from member", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">rmrole <@role> <@member>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def crole(self, ctx):
        embed_commands = discord.Embed(title="crole", description= "Create new role in Server", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">crole <rolename>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def drole(self, ctx):
        embed_commands = discord.Embed(title="drole", description= "Delete role from Server", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">drole <rolename>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def report(self, ctx):
        embed_commands = discord.Embed(title="Report", description= "Report user for a serious reason", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">report <@member> <reason>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def reports(self, ctx):
        embed_commands = discord.Embed(title="Reports", description= "Report history for the user", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">reports <@member>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def dreport(self, ctx):
        embed_commands = discord.Embed(title="dreport", description= "Remove reports from the user", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">dreport <@member>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def messages(self, ctx):
        embed_commands = discord.Embed(title="Messages", description= "List deleted messages", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">messages")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def dmessages(self, ctx):
        embed_commands = discord.Embed(title="dmessages", description= "Remove deleted messages", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">dmessages")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def nsfw(self, ctx):
        embed_commands = discord.Embed(title="NSFW", description= "NSFW content from reddit, **default sub is nsfw**", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">nsfw / >nsfw <subreddit>")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def server(self, ctx):
        embed_commands = discord.Embed(title="Server", description= "Fetch Server Informations", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">server")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def bot(self, ctx):
        embed_commands = discord.Embed(title="BOT", description= "Fetch BOT Informations", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">bot")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def who(self, ctx):
        embed_commands = discord.Embed(title="who", description= "Fetch User Informations", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">who")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def poll (self, ctx):
        embed_commands = discord.Embed(title="Poll ", description= "Ask a question, YES or NO", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">poll <question>")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def memes(self, ctx):
        embed_commands = discord.Embed(title="Memes", description= "Memes from reddit", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">memes")
        await ctx.send(embed=embed_commands)

def setup(bot):
    bot.add_cog(Help(bot))