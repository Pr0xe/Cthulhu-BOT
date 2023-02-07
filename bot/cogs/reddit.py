from logging import log
import praw
import random
import discord
from discord.ext import commands
from discord import Embed, Member
import constants
from discord import app_commands

class Reddit(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id='J7EILPujlzhsxQ',
                        client_secret='zOznJdN--fePXb9abkDGviS0RkO9rw',
                        user_agent='cthulhu-bot',
                        check_for_async=False)
    
    @commands.command(name="nsfw" ,description="Nsfw content at specific channel(18+)")
    @commands.has_role(constants.NSFW_ROLE_ID)
    async def nsfw(self, ctx, subred="nsfw"):
        if ctx.channel.is_nsfw():
            subbs = []
            
            hot_submissions = self.reddit.subreddit(subred).hot(limit=25)
            for submission in hot_submissions:
                subbs.append(submission)
           
            random_pick = random.choice(subbs)
            name = random_pick.title 
            url = random_pick.url
            
            await ctx.send(f"{name}\n{url}")

        else:
            embed=discord.Embed(title=":x: Channel Error", description="You need to be in NSFW channel to use this command", color=0xff0000)
            await ctx.reply(embed=embed)
    
    @nsfw.error
    async def addrole_error(self, ctx ,error):
        if isinstance(error, commands.MissingRole):
            embed=discord.Embed(title="Permission Denied.", description="No required role to use this command", color=0xff0000)
            await ctx.reply(embed=embed)
    
    @commands.command(name="memes", description="Fetch random meme from subbreddit <memes>")
    @app_commands.guilds(constants.SERVER_ID)
    async def memes(self, ctx):
        if not ctx.channel.is_nsfw():
            subbs = []
            
            hot_submissions = self.reddit.subreddit("memes").hot(limit=25)
            for submission in hot_submissions:
                subbs.append(submission)

            random_pick = random.choice(subbs)
            name = random_pick.title 
            url = random_pick.url
            
            await ctx.send(f"{name}\n{url}")
        else:
            embed=discord.Embed(title=":x: Channel Error", description="You are in NSFW channel. Try command away from here!", color=0xff0000)
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Reddit(bot))