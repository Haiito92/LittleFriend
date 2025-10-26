import discord
from discord.ext import commands
from discord import app_commands

from database.greetings_db import GreetingsDatabase


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = GreetingsDatabase()
        print("Greetings Cog Ready!")

    #Commands
    @app_commands.command(name="setwelcomechannel", description="Set the welcome channel.")
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need administrator permission to set welcome channel.", ephemeral=True)
            return

        self.db.set_guild_welcome_channel(interaction.guild.id, channel.id)
        await interaction.response.send_message(f"Welcome channel has been set to {channel.mention}!", ephemeral=True)


    @app_commands.command(name="setwelcomemessage", description="Set the welcome message.")
    async def set_welcome_message(self, interaction: discord.Interaction, message: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need administrator permission to set welcome message.",ephemeral=True)
            return

        self.db.set_guild_welcome_message(interaction.guild.id, message)
        await interaction.response.send_message(f"Welcome message has been set to :\n {message}", ephemeral=True)


    #Events
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel_id = self.db.get_guild_welcome_channel(member.guild.id)
        if channel_id is None:
            return

        channel = member.guild.get_channel(channel_id)
        if channel is None:
            return

        message = self.db.get_guild_welcome_message(member.guild.id)
        if message is not None:
            await channel.send(message)
        else:
            await channel.send(f"Welcome to {member.mention}! Enjoy your stay!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Greetings(bot))