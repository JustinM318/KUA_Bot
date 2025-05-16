import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import DBManagement

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
APP_ID = os.getenv('APPLICATION_ID')
GUILD_ID = os.getenv('GUILD_ID')

db_manager = DBManagement.DBManagement()
db_manager.dbCreation()

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents, application_id=APP_ID)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

async def birthday_check():
    birthday_cog = bot.get_cog("BirthdayCog")
    if birthday_cog:
        bot.loop.create_task(birthday_cog.birthday_checker())
    else:
        print("BirthdayCog not found!")

# Load the cogs from commands
async def load_cogs():
    try:
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                await bot.load_extension(f'commands.{filename[:-3]}')  # Load each cog
                print(f"Loaded {filename[:-3]} successfully.")
    except Exception as e:
        print(f"Failed to load cog: {e}")

# Start the bot
async def main():
    async with bot:
        await load_cogs()  # Load all cogs
        await birthday_check()  # Start the birthday checker
        await bot.start(TOKEN)

asyncio.run(main())