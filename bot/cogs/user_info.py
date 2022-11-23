import discord
from discord.ext import commands
from discord import Embed, Member
 
class User_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(pass_context=True, aliases=['whoami','who'])
    async def user_info(self, ctx, member: discord.Member = None):
        log_channel = self.bot.get_channel(900492686581178398)
        if not member:
            member = ctx.author
        
        name = member.display_name
        roles = [role for role in member.roles[1:]]
        em_user = discord.Embed(
            title=f"User info - {member}",
            colour=0xFFA500,
            timestamp=ctx.message.created_at)
        em_user.set_thumbnail(url=member.display_avatar)
        em_user.set_footer(text=f"Requested by {name}")
        fields = [
            ("Username", name),
            ("Created Account On:", member.created_at.strftime("%#d %B %Y")),
            ("Joined Server On:", member.joined_at.strftime("%#d %B %Y")),
            ("Roles:", "".join([role.mention for role in roles])),
            ("Highest Role:", member.top_role.mention),
        ]
        for name, value in fields:
            em_user.add_field(name=name, value=value)

        await ctx.send(embed=em_user)
        await log_channel.send(f"Informations about {member} printed: requested by {ctx.author}")

async def setup(bot):
    await bot.add_cog(User_info(bot))