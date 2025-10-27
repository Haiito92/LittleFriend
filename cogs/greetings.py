import discord
from discord.ext import commands
from discord import app_commands

from database.greetings_db import GreetingsDatabase


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = GreetingsDatabase()
        self.help_text = self._load_help_markdown()
        print("Greetings Cog Ready!")

    #Load files
    def _load_help_markdown(self) -> str:
        try:
            with open("docs/greetings.md", "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "Help markdown not found."


    #Command group
    greetings_commands = app_commands.Group(name="greetings", description="Greetings commands.")

    #Commands
    @greetings_commands.command(name="help", description="Get hints on how to call commands.")
    async def help(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need administrator permission to use this command.", ephemeral=True)
            return

        await interaction.response.send_message(self.help_text, ephemeral=True)

    @greetings_commands.command(name="info", description="Get information about the current greetings config.")
    async def info(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need administrator permission to use this command.", ephemeral=True)
            return

        # Get data
        channel_id = self.db.get_guild_welcome_channel(interaction.guild.id)
        welcome_message = self.db.get_guild_welcome_message(interaction.guild.id)

        # Format channel info
        if channel_id is not None:
            channel = interaction.guild.get_channel(channel_id)
            channel_info = channel.mention if channel else "⚠️ *Channel not found (may have been deleted)*"
        else:
            channel_info = "*Not set*"

        # Format message info
        message_info = f"{welcome_message}" if welcome_message else "*Not set*"

        # Build response using an embed (cleaner look)
        embed = discord.Embed(
            title="📋 Greetings Config",
            color=discord.Color.blue()
        )
        embed.add_field(name="Welcome Channel", value=channel_info, inline=False)
        embed.add_field(name="Welcome Message", value=message_info, inline=False)

        # Show example if message is set
        if welcome_message:
            example = self._format_welcome_message(interaction.user, welcome_message)
            embed.add_field(name="Preview", value=example, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


    @greetings_commands.command(name="setchannel", description="Set the welcome channel.")
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need administrator permission to set welcome channel.", ephemeral=True)
            return

        self.db.set_guild_welcome_channel(interaction.guild.id, channel.id)
        await interaction.response.send_message(f"Welcome channel has been set to {channel.mention}!", ephemeral=True)

    #Possible placeholders : {mention},{user],{server}
    @greetings_commands.command(name="setmessage", description="Set the welcome message.")
    @app_commands.describe(message="The message to be sent.")
    async def set_welcome_message(self, interaction: discord.Interaction, message: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need administrator permission to set welcome message.",ephemeral=True)
            return

        self.db.set_guild_welcome_message(interaction.guild.id, message)
        await interaction.response.send_message(f"Welcome message has been set to :\n {message}", ephemeral=True)

    #Possible placeholders : {mention},{user],{server}
    def _format_welcome_message(self, member: discord.Member, db_message: str) -> str:
        if '{mention}' in db_message:
            db_message = db_message.replace('{mention}', f'{member.mention}')
        if'{user}' in db_message:
            db_message = db_message.replace('{user}', f'{member.display_name}')
        if'{server}' in db_message:
            db_message = db_message.replace('{server}', f'{member.guild.name}')

        return db_message

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
            message = self._format_welcome_message(member, message)
            await channel.send(message)
        else:
            await channel.send(f"Welcome to {member.mention}! Enjoy your stay!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Greetings(bot))