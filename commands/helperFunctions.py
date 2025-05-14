import random
import discord
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands
        
class HelperFunction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="flipcoin", description="Flip a coin")
    async def flip_coin(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        result = random.choice(["Heads", "Tails"])
        await interaction.followup.send(f"The coin landed on: {result}")
        
    @app_commands.command(name="roll", description="Roll a die")
    @app_commands.describe(sides="Number of sides on the die")
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        await interaction.response.defer(thinking=True)
        if sides < 1:
            await interaction.followup.send("The number of sides must be at least 1.")
            return
        result = random.randint(1, sides)
        await interaction.followup.send(f"You rolled a {result} on a {sides}-sided die.")

async def setup(bot):
    await bot.add_cog(HelperFunction(bot))   
    # @app_commands.command(name="firstGoogleImage", description="Get the first Google image for a query")
    # @app_commands.describe(query="The search query")
    # async def first_google_image(self, interaction: discord.Interaction, query: str):
    #     await interaction.response.defer(thinking=True)
        
    #     await interaction.followup.send(f"First Google image for '{query}' would be displayed here.")