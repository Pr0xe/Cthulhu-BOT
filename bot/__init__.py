import asyncio
from sys import settrace, version
import discord
import json
import asyncpg
from glob import glob
from pathlib import Path
from discord import client
from discord.ext import commands
from discord.ext.commands import Bot as BotBase
from termcolor import colored
import constants
from discord import app_commands

COGS = [path.split("\\")[-1][:-3] for path in glob("./bot/cogs/*.py")]

async def get_prefix(self, message):
    with open("data/prefixes.json", 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")
    
    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

       
class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.guild = None
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=get_prefix,
                      help_command=None,
                      case_insensitive=True,
                      intents=discord.Intents.all())
    
    async def setup_hook(self):
        for cog in self._cogs:
            await self.load_extension(f"bot.cogs.{cog}")
            print((colored(f"{cog} LOADED!", 'green')))   
        print("setup completed")
    
    def run(self, version):
        self.VERSION = version

        with open("data/token.json", 'r', encoding="utf-8") as f:
            self.token = json.load(f)
        print("Running bot...")
        super().run(self.token["token"], reconnect=True)
    
    async def on_ready(self):
        channel = bot.get_channel(constants.LOG_CHANNEL)
        print(colored(f'Cthulhu has connected to Discord!', 'green'))
        await bot.change_presence(activity=discord.Game(name="?help"))
        await channel.send(f'`{self.user} has connected to Discord!`')

    async def on_member_join(self, member):
        channel = bot.get_channel(constants.WELCOME_CHANNEL)
        log_channel = bot.get_channel(constants.LOG_CHANNEL)
        user_embed = discord.Embed(
            colour=(discord.Colour.magenta()),
            title=':partying_face: Welcome :partying_face:',
            description=f'{member.mention} Welcome to **{member.guild.name}** Server !!'
        )
        await channel.send(embed=user_embed)
        role = discord.utils.get(member.guild.roles, id=constants.CUSTOM_ON_JOIN_ROLE_ID)
        await member.add_roles(role)
        await log_channel.send(f"{member} joined the server")

    async def on_member_remove(self, member):
        channel = bot.get_channel(constants.BYE_CHANNEL)
        bye_embed = discord.Embed(
            color=0x737373,
            title=':cross: Goodbye :cross:',
            description=f'{member} has left from the server!!'
        )
        await channel.send(embed=bye_embed)

bot = Bot()

@bot.command(name='sync')
async def reload(ctx):
    await ctx.send("Sync starting...")
    sy = await bot.tree.sync(guild=discord.Object(id=constants.SERVER_ID))
    await ctx.send(f"Sync completed: {len(sy)} commands synced ")

@bot.hybrid_command(name="test", with_app_command=True, description = "Testing")
@app_commands.guilds(discord.Object(id=constants.SERVER_ID))
@commands.has_permissions(administrator=True)
async def test(ctx: commands.Context):
    await ctx.defer(ephemeral=True)
    await ctx.reply("Hi!")