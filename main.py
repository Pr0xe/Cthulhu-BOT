import discord
import json
import asyncio
import asyncpg
import tracemalloc
import os
from discord.ext import commands
from threading import Thread
from termcolor import colored

tracemalloc.start()
with open("settings/token.json") as tok:
    tokens = json.load(tok)

async def get_prefix(client, message):
    with open("settings/prefixes.json", 'r') as f:
        prefixes = json.load(f)    
    return prefixes[str(message.guild.id)]

client = commands.Bot(  command_prefix = get_prefix, 
                        help_command = None,
                        case_insensitive = True, 
                        intents = discord.Intents.all(),
                    )
with open("settings/pass.json") as password:
    PASS = json.load(password)

async def create_db_pool():
    try:
        client.pg_con = await asyncpg.create_pool(database="discordbot", user="pr0xe", password=PASS["password"])
        print("Database opened successfully")
    except:
        print("Unable to connect")   


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name="@mention me for help"))

@client.event
async def on_message(msg):
    if not msg.author.bot:
        try:
            if msg.mentions[0] == client.user:
                with open("settings/prefixes.json", 'r') as f:
                    prefixes = json.load(f)    
                pre = prefixes[str(msg.guild.id)]
                await msg.channel.send(f"Find Information there `{pre}help`")
        except:
            pass
        #password remain
        try:
            if msg.content.startswith('password' or 'pass'):
                await msg.channel.send(f"{msg.author.mention} Don't say passwords!!")
        except:
            pass
        await client.process_commands(msg)

@client.event
async def on_command_error(ctx, error):
    try:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"{ctx.message.author.mention} Command not found")
            return
    except:
        pass    

@client.event
async def on_member_join(member):
    channel = client.get_channel(784492565239037973)
    user_embed = discord.Embed(
        colour = (discord.Colour.magenta()),
        title = ':partying_face: Welcome :partying_face:',
        description = f'{member.mention} Welcome to **{member.guild.name}** Server !!'
    )
    await channel.send(embed=user_embed)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(825767793102291024)
    bye_embed = discord.Embed(
        color=0x737373,
        title = ':cross: Goodbye :cross:',
        description = f'{member} has left from the server!!'
    )
    await channel.send(embed=bye_embed)


@client.event
async def on_guild_join(guild):
    with open('settings/prefixes.json','r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'cl.'
    with open('settings/prefixes.json','w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('settings/prefixes.json','r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('settings/prefixes.json','w') as f:
        json.dump(prefixes, f, indent=4)

if __name__ == '__main__':
    for file in os.listdir('cogs'):
        if file.endswith('.py'):
            client.load_extension(f'cogs.{file[:-3]}')
            print(colored(f"{file} LOADED!",'green'))


client.loop.run_until_complete(create_db_pool())
loop = asyncio.get_event_loop()
loop.create_task(client.run(tokens["token"]))
Thread(target=loop.run_forever())
