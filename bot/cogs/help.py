from discord.ext import commands
import discord
from discord.ui import View, Select
import constants
from discord import app_commands

class HelpSelect(Select):
    def __init__(self, bot: commands.Bot):
        super().__init__(
            placeholder="Choose a category",
            options=[
                discord.SelectOption(
                    label=cog_name, description=cog.__doc__
                )
                for cog_name, cog in bot.cogs.items() if cog.__cog_commands__ and cog_name not in ['Pr0xe']
            ]
        )

        self.bot = bot
    async def callback(self, interaction: discord.Interaction)->None:
        cog = self.bot.get_cog(self.values[0])
        assert cog

        commands_mixer = []
        for i in cog.walk_commands():
            if i == "prefix":
                pass
            commands_mixer.append(i)
        for i in cog.walk_app_commands():
            if i == "prefix":
                pass
            commands_mixer.append(i)
        
        embed = discord.Embed(
            title=f"{cog.__cog_name__} Commands",
            description='\n'.join(
                f"**{command.name}**: `{command.description}`"
                for command in commands_mixer
            )
        )
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="help", description="Show list of commands")
    @app_commands.guilds(constants.SERVER_ID)
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Help command",
            description="This is help command"
        )
        view = View().add_item(HelpSelect(self.bot))
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Utils(bot),guilds=[discord.Object(id=constants.SERVER_ID)])