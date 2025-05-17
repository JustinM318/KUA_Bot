import datetime
import sqlite3 
import discord
import asyncio
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

class BirthdayCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('KUA.db')
        self.cursor = self.db.cursor()
       
    async def getChannelID(self):
        load_dotenv()
        return os.getenv('KUA_CHANNEL_ID')
    
    async def birthday_converter(self, date_str):
        date_obj = datetime.datetime.strptime(date_str, '%m/%d')
        month = date_obj.strftime('%B')
        day = int(date_obj.strftime('%d'))
        if 11 <= day <= 13:
            suffix = "th"
        elif day % 10 == 1:
            suffix = "st"
        elif day % 10 == 2:
            suffix = "nd"
        elif day % 10 == 3:
            suffix = "rd"
        else:
            suffix = "th"
        return f"{month} {day}{suffix}"
        
    async def birthday_checker(self):
        await self.bot.wait_until_ready()  # Wait until the bot is ready
        print("Birthday checker task started.")
        while not self.bot.is_closed():
            # Get today's date in MM/DD format
            today = datetime.datetime.now().strftime('%m/%d')
            print(f"Today's date: {today}")

            # Query the database for today's birthdays
            self.cursor.execute('''
            SELECT user_id, birthday FROM users
            WHERE birthday LIKE ?
            ''', (f'{today}%',))
            birthdays = self.cursor.fetchall()

            # Send birthday messages if there are any
            if birthdays:
                for birthday in birthdays:
                    user_id = birthday[0]
                    user = await self.bot.fetch_user(user_id)
                    channel = await self.bot.fetch_channel(await self.getChannelID())
                    # Send a birthday message to specific channel
                    if channel and user:
                        print(f"Sending birthday message to {user.name} in channel {channel.name}.")
                        #await channel.send(f"Happy Birthday <@{user_id}>! 🎉🎂")
                        embed = discord.Embed(
                            title="Birthday alert!",
                            description=f"Happy Birthday <@{user_id}>! 🎉🎂",
                            color=discord.Color.blue()
                        )
                        embed.set_thumbnail(url=user.avatar.url)
                        embed.set_footer(text="Post any and all pictures to celebrate!")
                        file = discord.File("assets/happyBirthday.png")
                        embed.set_image(url="attachment://happyBirthday.png")            
                        embed.set_author(name="KUA Bot", icon_url=self.bot.user.avatar.url)
                        await channel.send(file = file, embed=embed)
                    else:
                        if channel is None:
                            print(f"Channel not found for ID: {user_id}")
                        if user is None:
                            print(f"User not found for ID: {user_id}")                   
            else:
                print("No birthdays today.")

            # Wait until the next day (24 hours)
            await asyncio.sleep(86400)


    @app_commands.command(name="registerbirthday", description="Register or update a birthday")
    @app_commands.describe(user="The user to register or update (only for admins)", birthday="The birthday in MM/DD format")
    async def register_birthday(self, interaction: discord.Interaction, birthday: str, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        permissions = interaction.channel.permissions_for(interaction.user)
        is_admin = permissions.administrator

        # If the user is not an admin, restrict them to editing their own birthday
        if not is_admin and user is not None:
            await interaction.followup.send("You are not allowed to register or update birthdays for other users!", ephemeral=True)
            return

        # Determine the target user (self if not admin or no user specified)
        target_user = user if is_admin and user is not None else interaction.user

        if not isinstance(birthday, str) or len(birthday) != 5 or birthday[2] != '/':
            await interaction.followup.send("Invalid birthday format. Please use MM/DD.", ephemeral=True)
            return
        
        try:
            # Check if the birthday already exists for the target user
            self.cursor.execute('''
            SELECT birthday FROM users WHERE user_id = ?
            ''', (target_user.id,))
            existing_birthday = self.cursor.fetchone()

            if existing_birthday[0]:
                # Update the birthday if it already exists
                self.cursor.execute('''
                UPDATE users SET birthday = ? WHERE user_id = ?
                ''', (birthday, target_user.id))
                self.db.commit()
                print(f"Updated birthday from {existing_birthday[0]} to {birthday} for {target_user.name}")
                await interaction.followup.send(f"Updated birthday for {target_user} to {await self.birthday_converter(birthday)}!")
            else:
                # Insert a new birthday if it doesn't exist
                self.cursor.execute('''
                UPDATE users 
                SET birthday = ?
                WHERE user_id = ?
                ''', (birthday, target_user.id))
                self.db.commit()
                print(f"Inserted new birthday for {target_user}: {birthday}")
                await interaction.followup.send(f"Registered birthday for {target_user}: {await self.birthday_converter(birthday)}!")
        except sqlite3.Error as e:
            print(e)
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="listbirthdays", description="List all registered birthdays")
    async def list_birthdays(self, interaction: discord.Interaction):
        # Defer interaction to show that the bot is processing
        await interaction.response.defer(thinking=True)

        try:
            # Query the database for all birthdays
            self.cursor.execute('''
            SELECT user_id, birthday FROM users
            ''')
            results = self.cursor.fetchall()
            for results.__len__ in results:
                birthday_list = "\n".join([f"<@{self.bot.fetch_user(user_id).name}>: {await self.birthday_converter(birthday)})" for user_id, birthday in results])
                print(f"Registered birthdays:\n{birthday_list}")
                # embed = discord.embed(
                #     title="Registered Birthdays",
                #     description=birthday_list,
                #     color=discord.Color.blue()
                # )
                await interaction.followup.send(f"Registered birthdays:\n{birthday_list}")
            else:
                print("No registered birthdays found.")
                await interaction.followup.send("No registered birthdays found.", ephemeral=True)
        except Exception as e:
            print (e)
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)
            
    @app_commands.command(name="deletebirthday", description="Delete a birthday")
    @app_commands.describe(user="The user whose birthday to delete (only for admins)")
    async def delete_birthday(self, interaction: discord.Interaction, user: discord.User = None):
        # Defer interaction to show that the bot is processing
        await interaction.response.defer(thinking=True)

        # Check if the user is an admin
        permissions = interaction.channel.permissions_for(interaction.user)
        is_admin = permissions.administrator

        # If the user is not an admin, restrict them to deleting their own birthday
        if not is_admin and user is not None:
            await interaction.followup.send("You are not allowed to delete birthdays for other users!", ephemeral=True)
            return

        # Determine the target user (self if not admin or no user specified)
        target_user = user if is_admin and user is not None else interaction.user

        try:
            # Delete the birthday for the target user
            self.cursor.execute('''
            DELETE FROM users WHERE user_id = ?
            ''', (target_user.id,))
            self.db.commit()

            if self.cursor.rowcount > 0:
                print(f"Deleted birthday for {target_user}.")
                await interaction.followup.send(f"Deleted birthday for {target_user}!")
            else:
                print(f"Deleted failed for {target_user}. No birthday found.")
                await interaction.followup.send(f"No birthday found for {target_user}.", ephemeral=True)
        except sqlite3.Error as e:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)
            
async def setup(bot):
    await bot.add_cog(BirthdayCommands(bot))