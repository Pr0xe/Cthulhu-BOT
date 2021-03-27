import discord
import platform
from discord.utils import get
from discord.ext import commands
from discord import Embed, Member

pr0xe_id = '<@188771015751368704>'

class BotInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(pass_context=True, name="BOT Info",aliases=['bot'])
    async def bot(self, ctx):
        embed = discord.Embed(
        title="BOT information",
        colour=0x1167B1)
        python_p = ["Python", platform.python_version() ]
        embed.set_author(name="Cthulhu ", icon_url="https://cdn.discordapp.com/app-icons/766607810943123466/97bc49d97193d6de74c7a8f9b3a1c8ef.png?size=256")
        embed.set_image(url="https://cdn.discordapp.com/app-icons/766607810943123466/97bc49d97193d6de74c7a8f9b3a1c8ef.png?size=256")
        fields = [  ("Bot Developer", pr0xe_id, False),
                    ("Programming Language", f"{python_p[0]}  {python_p[1]}",True ),
                    ("Server counter", len(self.client.guilds),True),
                    ("Discord Version", discord.__version__,False),
                    ("Latency", f"{round(self.client.latency * 1000)}ms", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)           
        await ctx.send(embed=embed)
        print("BOT Infos are DONE")
def setup(client):
    client.add_cog(BotInfo(client))