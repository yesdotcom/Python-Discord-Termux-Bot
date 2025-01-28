import discord
from discord.ext import commands
import aiohttp
import asyncio, logging
class battery(commands.Cog):
    logging = logging.getLogger('main.py')
    def __init__(self, client: commands.Bot, config: dict, currentDir: str):
        self.client = client
        self.config = config
        self.currentDir = currentDir

    async def bat_cog(self):
        """
        Updates the bot's status with the phone's battery percentage
        by querying a Flask API.
        """
        flask_api_url = "http://10.0.0.157:5000/battery"  # Replace with your Flask API URL
        while True:
            await asyncio.sleep(5)  # Wait for the bot to fully connect to Discord
            logging.info("Bot connected to Discord, starting battery status update loop.")
            async with aiohttp.ClientSession() as session:
                try:
                    logging.info("Sending request to Flask API for battery status.")
                    async with session.get(flask_api_url) as resp:
                        logging.info(f"Received response from Flask API. Status: {resp.status}")  
                        if resp.status == 200:
                            data = await resp.json()
                            battery_percentage = data.get("percentage", "Unknown")
                            logging.info(f"Battery percentage fetched: {battery_percentage}%")
                            status = f"🔋 {battery_percentage}%"
                            await self.bot.change_presence(
                                activity=discord.Game(name=status)
                            )
                            logging.info("Bot status updated with new battery percentage.")
                            await asyncio.sleep(60)  # Update every minute
                        else:
                            logging.error(f"Failed to fetch battery data. Status: {resp.status}")
                except Exception as e:
                    logging.error(f"An error occurred while updating bot status: {e}")