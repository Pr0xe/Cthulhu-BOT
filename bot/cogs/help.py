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
        embed_commands.add_field(name="Community", value="`who`, `server`, `bot`, `poll`, `memes`, `level`, `board`, `nsfw(+18)`", inline= False)
        embed_commands.add_field(name="Reporting System", value="`report`, `reports`", inline= False)
        embed_commands.add_field(name="Music", value="`play`, `pause`, `stop`, `skip`, `queue`, `restart`, `playing`, `leave`, `shuffle`", inline= False)
        embed_commands.add_field(name="Moderation - :no_entry: Only for Admins and Owner :no_entry:", value="`cprefix`, `clear`,`cleardb`, `ban`, `unban`, `kick`, `mute`, `unmute`, `role`, `rmrole`, `crole`, `drole`, `dreport`, `rmlevel`", inline= False) 
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
    
    @help.command()
    async def play(self, ctx):
        embed_commands = discord.Embed(title="Play", description= "Play music on your voice channel, or to continue paused song", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">play or p <name of song>")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def pause(self, ctx):
        embed_commands = discord.Embed(title="Pause", description= "Pause song", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">pause")
        await ctx.send(embed=embed_commands)
    
    
    @help.command()
    async def queue(self, ctx):
        embed_commands = discord.Embed(title="Queue", description= "Print list of Queue", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">queue or q")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def leave(self, ctx):
        embed_commands = discord.Embed(title="Leave", description= "Disconnect bot from voice channel", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">leave")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def playing(self, ctx):
        embed_commands = discord.Embed(title="Playing Now", description= "Print info about current playing song", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">playing or np")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def stop(self, ctx):
        embed_commands = discord.Embed(title="Stop", description= "Stop music and reset queue", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">stop")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def restart(self, ctx):
        embed_commands = discord.Embed(title="Restart", description= "Restart current track", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">restart")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def shuffle(self, ctx):
        embed_commands = discord.Embed(title="Shuffle", description= "Shuffle the song queue", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">shuffle")
        await ctx.send(embed=embed_commands)
    
    @help.command()
    async def board(self, ctx):
        embed_commands = discord.Embed(title="Level leaderboard", description= "Print out the Level XP leaderboard of users", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">board")
        await ctx.send(embed=embed_commands)

    @help.command()
    async def cleardb(self, ctx):
        embed_commands = discord.Embed(title="Clear Database", description= "Clear Database from users that left the server", color= ctx.author.color)
        embed_commands.add_field(name="**Syntax**", value=f">cleardb")
        await ctx.send(embed=embed_commands)

async def setup(bot):
    await bot.add_cog(Help(bot))
