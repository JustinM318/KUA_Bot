import random
import discord
import time
import sqlite3
from discord import app_commands
from discord.ext import commands

class PokemonFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('KUA.db')
        self.cursor = self.db.cursor()
        
    @app_commands.command(name="registerfavoritepokemon", description="Sets a favorite pokemon")
    async def setfavoritepokemon(self, interaction: discord.Interaction, favepokemon: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        username = interaction.user.name

        if favepokemon is None:
            await interaction.followup.send("Please provide a Pokémon name.", ephemeral=True)
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
        await interaction.followup.send(f"{username}'s favorite Pokémon has been set to: {favePKMN}")

async def setup(bot):
    await bot.add_cog(PokemonFunctions(bot))  