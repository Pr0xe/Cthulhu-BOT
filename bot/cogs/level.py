import discord
import asyncio
import asyncpg
import nest_asyncio
import json
from termcolor import colored
from discord import embeds
from discord.ext import commands
from discord import Embed, Member
import constants
from discord import app_commands

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.run_until_complete(self.create_db_pool())

    @commands.Cog.listener()
    async def on_ready(self):
        await self.pg_con.execute("CREATE TABLE IF NOT EXISTS levels (user_id character varying, guild_id character varying, level int, xp int)")
        print("leveling system ready") 

    async def create_db_pool(self):
        try:
            with open("data/pass.json") as password:
                PASS = json.load(password)
            self.pg_con = await asyncpg.create_pool(database="discordbot", user="pr0xe", password=PASS["password"])
            print(colored("Level database opened successfully", 'cyan'))
        except:
            print(colored("Unable to connect", 'red'))

    async def level_up(self, user):
        cur_xp = user['xp']
        cur_level = user['level']

        if cur_xp >= round((4 * (cur_level ** 3)) / 5):
            await self.pg_con.execute("UPDATE levels SET level = $1 WHERE user_id = $2 AND guild_id = $3", cur_level + 1, user['user_id'], user['guild_id'])
            return True
        else:
            return False
        
    @commands.Cog.listener()
    async def on_message(self, ctx): 
        if ctx.author == self.bot.user:
            return

        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)

        user = await self.pg_con.fetch("SELECT * FROM levels WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        
        if not user:
            await self.pg_con.execute("INSERT INTO levels (user_id, guild_id, level, xp) VALUES ($1, $2, 1, 0)", author_id, guild_id)

        user = await self.pg_con.fetchrow("SELECT * FROM levels WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        await self.pg_con.execute("UPDATE levels SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 1, author_id, guild_id)
       
        if await self.level_up(user):
            channel = self.bot.get_channel(constants.LEVEL_CHANNEL)
            embed=discord.Embed(title=f":tada: Level Up :tada:", description="**{0}** is level **{1}** :star:".format(ctx.author.mention, user['level'] + 1), color=0x00ffff)
            await channel.send(embed=embed)
        
    @commands.hybrid_command(name="level", with_app_command=True ,description="Display the level of user")
    @app_commands.guilds(constants.SERVER_ID)
    async def level(self, ctx, member: discord.Member=None):
        
        if member is None:
            embed=discord.Embed(title="Argument Missing", description="Please mention username.", color=0xff0000)
            return await ctx.reply(embed=embed)

        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.pg_con.fetch("SELECT * FROM levels WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        if not user:
            embed = discord.Embed(
                title=f"User Level - {member}",
                color=0x29aff2, 
                timestamp=ctx.message.created_at
                )
            embed.set_thumbnail(url=member.display_avatar)
            embed.set_footer(text=f"Requested by {ctx.author}")
            embed.add_field(name="Level", value=f"No level Found")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title=f"User Level - {member}",
                color=0x29aff2, 
                timestamp=ctx.message.created_at
                )
            embed.set_thumbnail(url=member.display_avatar)
            embed.set_footer(text=f"Requested by {ctx.author}")
            embed.add_field(name="Level", value=user[0]['level'])
            embed.add_field(name="Total XP", value=user[0]['xp'])
            embed.add_field(name="XP to next Level", value=((round((4 * (user[0]['level'] ** 3)) / 5)) - (user[0]['xp'])), inline=False)
            await ctx.reply(embed=embed)

    @commands.hybrid_command(name="board", with_app_command=True ,description="Display the leaderboard of the server")
    @app_commands.guilds(constants.SERVER_ID)
    async def board(self, ctx):
        _data = await self.pg_con.fetch("SELECT * FROM levels ORDER BY level DESC")
        embed = discord.Embed(title=":crown: Level - XP Leaderboard :crown:", color=0x29aff2)
        for i in range(len(_data)):
            embed.add_field(name=f"{self.bot.get_user(int(_data[i][0]))}", value=f"level : {int(_data[i][2])}  XP : {int(_data[i][3])}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="cleardb", with_app_command=True ,description="Clear database from users that left the server")
    @app_commands.guilds(constants.SERVER_ID)
    @commands.has_permissions(ban_members=True)
    async def cleardb(self, ctx):
        _data = await self.pg_con.fetch("SELECT * FROM levels")
        for i in range(len(_data)):
            if self.bot.get_user(int(_data[i][0])) == None:
                none_field = _data[i][0]
                await self.pg_con.execute("DELETE FROM levels WHERE user_id = $1", none_field)
        await ctx.reply("Dead members cleared from Database")
    
    @cleardb.error
    async def cleardb_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="You have no permission to use this command.", color=0xff0000)
            await ctx.reply(embed=embed)

    @commands.hybrid_command(name="rmlevel", with_app_command=True ,description="Remove level of the user")
    @app_commands.guilds(constants.SERVER_ID)
    @commands.has_permissions(ban_members=True)
    async def rmlevel(self, ctx, member: discord.Member):
        log_channel = self.bot.get_channel(900492686581178398)
        embed = discord.Embed(
                colour=0xFFA500,
                timestamp=ctx.message.created_at)
        if not member:
            await ctx.reply(f"Please specify user")
            return
        else:
            member_id = str(member.id)
            await self.pg_con.execute("DELETE FROM levels WHERE user_id = $1", member_id)
            embed.add_field(name="Level Message", value=f"{ctx.message.author.mention} removed level from {member}", inline=True)
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)
            await log_channel.send(f"{ctx.message.author.mention} removed level from {member.mention}")

    @rmlevel.error
    async def rmlevel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="You have no permission to use this command.", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="ERROR", description="Arguments Missing", color=0xff0000)
            await ctx.reply(embed=embed)
async def setup(bot):
    await bot.add_cog(Levels(bot),guilds=[discord.Object(id=constants.SERVER_ID)])