import sqlite3
from flask import jsonify
import pandas as pd
import requests
import random
import discord
import time
from discord import app_commands
from discord.ext import commands

class PocketTCGCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('KUA.db')
        self.cursor = self.db.cursor()
        
    @app_commands.command(name='set_friendcode', description='Set your pocket TCG friend ID')
    async def setpockettcgfriendid(self, interaction: discord.Interaction, friendid: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            self.cursor.execute('''
            UPDATE users 
            SET pocketTCG_FriendID = ?
            WHERE user_id = ?''', (friendid, interaction.user.id))
        except Exception as e:
            print(e)
            await interaction.followup.send('There was an error adding FriendID.', ephemeral=True)
            return
        await interaction.followup.send('Successfully added FriendID.', ephemeral=True)
        
    @app_commands.command(name='get_friendcode', description='Get a friend ID for a user.')
    async def getPocketTCGFriendID(self, interaction: discord.Interaction, user: discord.User = None):
        # Determine the target user (self if no user specified)
        if user == None:
            lookupUser = interaction.user
        else:
            lookupUser = user
        try:
            self.cursor.execute('''
            SELECT pocketTCG_FriendIDusers 
            FROM users
            WHERE user_id = ?''', (lookupUser.id,))
            friendID = self.cursor.fetchone()      
        except Exception as e:
            print(e)
            await interaction.followup.send('There was an error getting FriendID.', ephemeral=True)
            return
        await interaction.followup.send(f'{lookupUser.name}\'s FriendID is {friendID}', ephemeral=True)
                  
async def setup(bot):
    await bot.add_cog(PocketTCGCommands(bot))