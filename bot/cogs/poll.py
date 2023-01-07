import discord
from discord.ext import commands
from discord import Embed, Member

class Poll(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context=True, name="Poll")
    async def poll(self, ctx, *, message):
        embed = discord.Embed(title=" :loudspeaker: POLL :loudspeaker: ", description=f"{message}", colour=0x29ddf2)
        msg = await ctx.channel.send(embed=embed)
        emoji = ['\N{THUMBS UP SIGN}','\N{THUMBS DOWN SIGN}']
        for em in emoji:
            await msg.add_reaction(em)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="ERROR", description="Arguments Missing", color=0xff0000)
            await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(Poll(client))