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

PREFIX = "cl."
COGS = [path.split("\\")[-1][:-3] for path in glob("./bot/cogs/*.py")]

async def get_prefix(bot, message):
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
        self.cogs_ready = Ready()
        self.guild = None
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=get_prefix,
                      help_command=None,
                      case_insensitive=True,
                      intents=discord.Intents.all())
    
    def setup(self):
        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print((colored(f"{cog} LOADED!", 'green')))
        print("setup completed")
    
    def run(self, version):
        self.VERSION = version
        print("running setup...")
        self.setup()

        with open("data/token.json", 'r', encoding="utf-8") as f:
            self.token = json.load(f)
        print("Running bot...")
        super().run(self.token["token"], reconnect=True)
    
    async def on_connect(self):
        print(colored(f'Cthulhu has connected to Discord!', 'red')) 
        await bot.change_presence(activity=discord.Game(name="cl.help"))

    async def on_member_join(member):
        channel = bot.get_channel(784492565239037973)
        log_channel = bot.get_channel(900492686581178398)
        user_embed = discord.Embed(
            colour=(discord.Colour.magenta()),
            title=':partying_face: Welcome :partying_face:',
            description=f'{member.mention} Welcome to **{member.guild.name}** Server !!'
        )
        await channel.send(embed=user_embed)
        role = discord.utils.get(member.guild.roles, id=831109657094520843)
        await member.add_roles(role)
        await log_channel.send(f"{role.mention} role added to {member.mention}")


    async def on_member_remove(member):
        channel = bot.get_channel(825767793102291024)
        bye_embed = discord.Embed(
            color=0x737373,
            title=':cross: Goodbye :cross:',
            description=f'{member} has left from the server!!'
        )
        await channel.send(embed=bye_embed)

async def create_db_pool():
        try:
            with open("data/pass.json") as password:
                PASS = json.load(password)
            Bot.pg_con = await asyncpg.create_pool(database="discordbot", user="pr0xe", password=PASS["password"])
            print(colored("Database opened successfully", 'cyan'))
        except:
            print("Unable to connect")

loop = asyncio.get_event_loop()
loop.run_until_complete(create_db_pool())  

bot = Bot()