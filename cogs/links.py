import discord
from discord.ext import commands
from discord import Embed, Member

class Links(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        channel = self.client.get_channel(762248895580733442)
        
        if ('http' or 'https' in message.content) and (message.channel == channel):
            embed=discord.Embed(title=":warning: Message Deleted :warning:", description=f"{message.author.mention} Links not allowed in this channel", color=0xff00f6)
            await channel.purge(limit=1)
            await channel.send(embed=embed)
            print(f"{message.author} posted a link, message deleted")
            return

def setup(client):
    client.add_cog(Links(client))
