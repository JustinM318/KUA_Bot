import random
import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
        
class HelperFunction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('KUA.db')
        self.cursor = self.db.cursor()

    @app_commands.command(name="register", description="Register yourself in the database")
    async def register_user(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        user_id = interaction.user.id
        username = interaction.user.name

        # Check if the user is already registered
        try:
            self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)
            return

        if result:
            await interaction.followup.send(f"You are already registered.", ephemeral=True)
            return

        try:
            self.cursor.execute('''
                INSERT INTO users (user_id) VALUES (?)
            ''', (user_id))
        except Exception as e:
            print(e)
            await interaction.followup.send(f"An error occurred while registering: {e}", ephemeral=True)
            return
        
        self.db.commit()
        
        await interaction.followup.send(f"Successfully registered {username}!", ephemeral=True)
        
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
        
    @app_commands.command(name="setfavoritepokemon", description="Sets a favorite pokemon")
    async def setfavoritepokemon(self, interaction: discord.Interaction, favepokemon: str):
        await interaction.response.defer(thinking=True)

        if favepokemon is None:
            await interaction.followup.send("Please provide a Pokémon name.")
            return

        try:
            self.cursor.execute('''
            UPDATE users SET favoritePokemon = ? WHERE user_id = ?
            ''', (favepokemon, interaction.user.id))
        except Exception as e:
            print(e)
            await interaction.followup.send(f"An error occurred setting favorite pokemon: {e}", ephemeral=True)
            return
   
        self.db.commit()
        await interaction.followup.send(f"Your favorite Pokémon has been set to: {favePKMN}", ephemeral=True)



async def setup(bot):
    await bot.add_cog(HelperFunction(bot))   
    # @app_commands.command(name="firstGoogleImage", description="Get the first Google image for a query")
    # @app_commands.describe(query="The search query")
    # async def first_google_image(self, interaction: discord.Interaction, query: str):
    #     await interaction.response.defer(thinking=True)
        
    #     await interaction.followup.send(f"First Google image for '{query}' would be displayed here.")