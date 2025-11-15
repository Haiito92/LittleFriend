import discord
from aiohttp.web_routedef import options
from discord.ext import commands
from discord import app_commands
from discord import ui
from datetime import datetime

class TimestampFormatSelect(ui.Select):
    def __init__(self, timestamp: int, select_message : str):
        self.timestamp = timestamp
        self.select_message = select_message

        format_options = [
            discord.SelectOption(label="Short Time", value="t"),
            discord.SelectOption(label="Long Time", value="T"),
            discord.SelectOption(label="Short Date", value="d"),
            discord.SelectOption(label="Long Date", value="D"),
            discord.SelectOption(label="Short Date/Time", value="f"),
            discord.SelectOption(label="Long Date/Time", value="F"),
            discord.SelectOption(label="Relative Time", value="R"),
        ]

        super().__init__(placeholder="Choose a timestamp format...", options=format_options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        format_type = self.values[0]
        timestamp_string = f"`<t:{self.timestamp}:{format_type}>`"

        await interaction.response.send_message(f"{self.select_message}: {timestamp_string}\n", ephemeral=True)


class TimestampFormatView(ui.View):
    def __init__(self, timestamp: int, select_message : str):
        super().__init__()
        self.add_item(TimestampFormatSelect(timestamp, select_message))

class TimestampModal(ui.Modal, title="Enter a Data and Time"):
    date_input = ui.TextInput(label="Date (DD/MM/YYYY)", placeholder="01/01/2025")
    time_input = ui.TextInput(label="Time (HH:MM)", placeholder="12:00")

    async def on_submit(self,interaction: discord.Interaction):

        try:
            date_time = datetime.strptime(f"{self.date_input.value} {self.time_input.value}", "%d/%m/%Y %H:%M")
            timestamp = int(date_time.timestamp())

            timestamp_format_view = TimestampFormatView(timestamp, "Here is the Unix timestamp for your custom time")
            await interaction.response.send_message(f"Select a timestamp format:", view=timestamp_format_view, ephemeral=True)
        except:
            await interaction.response.send_message("Invalid Format! Use DD/MM/YY and HH:MM.\n", ephemeral=True)

class Timestamps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Timestamps Cog Ready!")

    #Command group
    timestamps_command = app_commands.Group(name="timestamps", description="Timestamps commands")

    @timestamps_command.command(name="current_time")
    async def current_time(self, interaction: discord.Interaction):

        current_time : int = int(datetime.now().timestamp())

        timestamp_format_view = TimestampFormatView(current_time, "Here is the Unix timestamp for your current time")
        await interaction.response.send_message(f"Select a timestamp format:", view=timestamp_format_view, ephemeral=True)

    @timestamps_command.command(name="custom_time")
    async def custom_time(self, interaction: discord.Interaction):

        timestamp_modal = TimestampModal()
        await interaction.response.send_modal(timestamp_modal)

async def setup(bot: commands.Bot):
    await bot.add_cog(Timestamps(bot))