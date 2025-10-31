import discord
from discord.ext import commands
from discord import app_commands
import requests

class Jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Command group
    jokes_command = app_commands.Group(name="jokes", description="Jokes commands")

    def _get_joke(self) -> str:
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})

        if response.status_code == 200:
            data = response.json()
            return f"{data['joke']}"
        else:
            return "I can't think of a joke at the moment 😅"


    @jokes_command.command(name="joke")
    async def joke(self, interaction: discord.Interaction):
        await interaction.response.send_message(self._get_joke(), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Jokes(bot))