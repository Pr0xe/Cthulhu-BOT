import discord
import json
from discord.ext import commands
from discord import Embed, Member

class Help(commands.Cog):
    def __init__(self,client):
        self.client = client
        
    @commands.command(pass_context = True)
    async def help(self, ctx):
        with open("settings/prefixes.json", 'r') as f:
                prefixes = json.load(f)    
        pre = prefixes[str(ctx.guild.id)]
        embed_commands = discord.Embed(
            colour = 0x00FF00,
            title = "Commands",
            description = f"Prefix for this server is `{pre}`"
        )
        fields = [  ("```advanced```", 'Server moderation commands', False), 
                    ("```server```", 'Fetch Server Informations', False),
                    ("```bot```", 'Fetch BOT Informations', False),
                    ("```who```", 'Fetch User Informations', False),
                    ("```level```", 'Check out your level in server', False),
                    ("```poll <question>```", 'Ask a question, YES or NO', False),
                    ("```memes```", 'Memes from reddit', False),
                ]
        
        for name, value, inline in fields:
            embed_commands.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed_commands)

def setup(client):
    client.add_cog(Help(client))