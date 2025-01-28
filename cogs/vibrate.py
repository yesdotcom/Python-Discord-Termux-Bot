import discord
from discord.ext import commands
from discord.ext import commands
from discord.app_commands import guild_only, command, describe
import aiohttp
import logging
class vibrate(commands.Cog):
    logging = logging.getLogger('main.py')
    def __init__(self, client: commands.Bot, config: dict, currentDir: str):
        self.client = client
        self.config = config
        self.currentDir = currentDir

    @command(name="vibrate", description="Vibrate phone for a duration.")
    @guild_only()
    @describe(duration="In seconds")
    async def vibrate_command(self, interaction: discord.Interaction, duration: int):
        await interaction.response.defer(ephemeral=False)
        if duration > 3:
            await interaction.followup.send("Vibration duration cannot exceed 3 seconds.")
            return
        flask_api_url = "http://10.0.0.157:5000/vibrate"  # Replace with your Flask API URL
        async with aiohttp.ClientSession() as session:
            try:
                logging.info(f"Sending POST request to Flask API with duration: {duration}")
                async with session.post(flask_api_url, json={"duration": duration}) as resp:
                    logging.info(f"Received response from Flask API. Status: {resp.status}")
                    if resp.status == 200:
                        await interaction.followup.send(f"Vibrate command sent successfully for {duration} seconds.")
                    else:
                        await interaction.followup.send(f"Failed to send vibrate command. Status: {resp.status}")
                        logging.error(f"Failed to send vibrate command. Status: {resp.status}")
            except Exception as e:
                if isinstance(e, discord.errors.NotFound):
                    await interaction.followup.send("Failed to send vibrate command. Webhook not found.")
                    logging.error("Failed to send vibrate command. Webhook not found.")
                else:
                    await interaction.followup.send(f"An error occurred while sending vibrate command: {e}")
                    logging.error(f"An error occurred while sending vibrate command: {e}")
