import wavelink
import discord
from discord import player
from discord import client
from discord.ext.commands import context
from discord.ext.commands.core import command
from discord.ext import commands
from discord import embeds

class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self,client):
        self.client = client
        self.wavelink = wavelink.Client(client=client)
        self.client.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.client and after.channel is None:
            if not [m for m in before.channel.members if not m.client]:
                pass

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node `{node.identifier}` ready.")

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs")
            return False
        return True

    async def start_nodes(self):
        await self.client.wait_until_ready()

        nodes = {
            "MAIN":{
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "regiom": "europe",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)
        
    def get_player(self, obj):
        if isinstance(obj, command.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

def setup(client):
    client.add_cog(Music(client))