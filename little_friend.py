import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

#Env variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

#Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

#Create my bot commands
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} has connected to Discord!")

keep_alive()
bot.run(TOKEN)