import discord
from discord.ext import commands
from discord import Embed, Member

class Links(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        log_channel = self.client.get_channel(900492686581178398)
        if message.author == self.client.user:
            return
        admin_channel = self.client.get_channel(762248895580733442)
        
        links = ['http', 'https']
        message_con = message.content
        for text in links:
            if ( text in message_con) and (message.channel == admin_channel):
                author_id = str(message.author)
                author = await self.client.pg_con.fetch("SELECT * FROM deleted_messages WHERE author_id = $1",author_id)
                if not author:
                    await self.client.pg_con.execute("INSERT INTO deleted_messages (author_id, messages) VALUES($1, ARRAY[$2])", author_id, message_con)
                    embed=discord.Embed(title=":warning: Message Deleted :warning:", description=f"{message.author.mention} Links not allowed in this channel", color=0xff00f6)
                else:
                    await self.client.pg_con.execute("UPDATE deleted_messages SET messages = array_append(messages, $1) WHERE author_id = $2",message_con,author_id)
                    embed=discord.Embed(title=":warning: Message Deleted :warning:", description=f"{message.author.mention} Links not allowed in this channel", color=0xff00f6)
                await admin_channel.purge(limit=1)
                await admin_channel.send(embed=embed)
                await log_channel.send(f"{message.author} posted a link, message deleted")
                return
    
    @commands.command(pass_context = True)
    @commands.has_permissions(ban_members=True)
    async def messages(self, ctx):
        deleted_embed = discord.Embed(
                title=":recycle: Deleted messages :recycle:",
                colour=0xFF0000)     
        counter = await self.client.pg_con.fetch("SELECT COUNT(*) AS RowCnt FROM deleted_messages")
        if counter==0:
            clear_embed = discord.Embed(
                title=":recycle: Deleted messages :recycle:",
                colour=0xFF0000)
            await ctx.send(embed=clear_embed)
            return
        else:
            rows = await self.client.pg_con.fetch("SELECT messages FROM deleted_messages")
            new_list=[]
            new_list.append(rows)
            deleted_embed.add_field(name="Deleted Message History", value=f"{new_list}", inline=False)
            await ctx.send(embed=deleted_embed)
            return
    @commands.command(pass_context = True)
    @commands.has_permissions(ban_members=True)
    async def dmessages(self, ctx):
        counter = await self.client.pg_con.fetch("SELECT COUNT(*) AS RowCnt FROM deleted_messages")
        if counter==0:
            clear_embed = discord.Embed(
                title=":recycle: Deleted messages :recycle:",
                colour=0xFF0000)
            await ctx.send(embed=clear_embed)
            return
        else:
            drep_embed = discord.Embed(
                title=":recycle: Message history cleared :recycle:",
                colour=0xFF0000)
            await self.client.pg_con.execute("DELETE FROM deleted_messages")
            await ctx.send(embed=drep_embed)


def setup(client):
    client.add_cog(Links(client))
