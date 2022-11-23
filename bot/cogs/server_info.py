import discord
from discord.ext import commands
from discord import Embed, Member

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="Server Info", aliases=['server'])
    async def server(self, ctx):
        log_channel = self.bot.get_channel(900492686581178398)
        embed = discord.Embed(
            title="Server informations",
            colour=discord.Color.random(),
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name} ")
        guild = ctx.guild
        statuses = [len(list(filter(lambda m: str(m.status) == "online",guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle",guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd",guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline",guild.members)))]

        fields = [("Server Name", guild.name, True),
                ("Server Owner", f'{guild.owner.mention}', True),
                ("Created at", guild.created_at.strftime("%d/%m/%Y"), True),
                ("Members", guild.member_count, True),
                ("Humans", len(list(filter(lambda m: not m.bot,guild.members))),True),
                ("Bots", len(list(filter(lambda m: m.bot,guild.members))), True), 
                ("Roles", len(ctx.message.guild.roles), True),
                ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", False)]   

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)
        await log_channel.send(f"Server informations printed : requested by {ctx.author}")

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
