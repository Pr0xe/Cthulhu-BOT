import discord
import platform
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Cog
from discord import Embed, Member
import constants
from discord import app_commands

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="bot", with_app_command=True ,description="Print information about the bot")
    @app_commands.guilds(constants.SERVER_ID)
    async def bot(self, ctx):
        log_channel = self.bot.get_channel(constants.LOG_CHANNEL)
        embed = discord.Embed(
        title="BOT information",
        colour=0x1167B1,
        timestamp=ctx.message.created_at)
        python_p = ["Python", platform.python_version()]
        embed.set_author(name="Cthulhu ", icon_url="https://cdn.discordapp.com/app-icons/766607810943123466/97bc49d97193d6de74c7a8f9b3a1c8ef.png?size=256")
        embed.set_footer(text=f"Requested by {ctx.author}")
        fields = [  ("Bot Developer", "[Pr0xe](https://pr0xe.github.io/)", False),
                    ("Programming Language", f"{python_p[0]}  {python_p[1]}",True ),
                    ("Discord.py Version", discord.__version__,False),
                    ("Github Repository", "[github.com/Pr0xe/Cthulhu-BOT](https://github.com/Pr0xe/Cthulhu-BOT)", False),
                    ("Latency", f"{self.bot.latency * 1000:,.0f}ms", True),
                   ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)
        await log_channel.send(f"BOT Infos printed : requested by {ctx.author.mention}")
    
async def setup(bot):
    await bot.add_cog(BotInfo(bot),guilds=[discord.Object(id=constants.SERVER_ID)])