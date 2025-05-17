import random
import discord
import time
import sqlite3
from functions.userFunctions import UserFunctions 
from discord import app_commands
from discord.ext import commands

class PokemonCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('KUA.db')
        self.cursor = self.db.cursor()
        
    @app_commands.command(name="registerfavoritepokemon", description="Sets a favorite pokemon")
    async def setfavoritepokemon(self, interaction: discord.Interaction, favepokemon: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        username = interaction.user.name
        user_id =  interaction.user.id
        
        if favepokemon is None:
            await interaction.followup.send("Please provide a Pokémon name.", ephemeral=True)
            return
        
        uf = UserFunctions()
        user = uf.getUser(user_id)
        
        if user == 1:
            try:
                self.cursor.execute('''
                UPDATE users SET favoritePokemon = ? WHERE user_id = ?
                ''', (favepokemon, user_id))                    
            except Exception as e:
                print(e)
                await interaction.followup.send(f"An error occurred setting favorite pokemon: {e}", ephemeral=True)
                return
            self.db.commit()
            print(f"{username}'s favorite Pokémon has been set to: {favepokemon}")
            await interaction.followup.send(f"{username}'s favorite Pokémon has been set to: {favepokemon}")
        else:
            print('No user found.')
            await interaction.followup.send(f"An error occured.")

async def setup(bot):
    await bot.add_cog(PokemonCommands(bot))  