from logging import log
import praw
import random
import discord
from discord.ext import commands
from discord import Embed, Member

class Reddit(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id='J7EILPujlzhsxQ',
                        client_secret='zOznJdN--fePXb9abkDGviS0RkO9rw',
                        user_agent='cthulhu-bot',
                        check_for_async=False)
    
    @commands.command(pass_context = True, aliases=['horny'])
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
            embed=discord.Embed(title=":x: Channel Error", description=f"{ctx.message.author.mention} You need to be in NSFW channel to use this command", color=0xff00f6)
            await ctx.send(embed=embed)
            print("nsfw channel error")
    
    @commands.command(pass_context = True, aliases=['meme'])
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
            embed=discord.Embed(title=":x: Channel Error", description=f"{ctx.message.author.mention} You are in NSFW channel. Try command away from here!", color=0xff00f6)
            await ctx.send(embed=embed)
            print("nsfw channel error")

async def setup(bot):
    await bot.add_cog(Reddit(bot))