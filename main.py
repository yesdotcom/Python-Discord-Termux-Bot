# Added logging
import discord, json, os, tracemalloc, asyncio
import logging
from discord.ext import commands
from cogs.cat import cat
from cogs.bat import battery
from cogs.vibrate import vibrate

tracemalloc.start()

# Configure logging
print("Loading logging...")
logging.basicConfig(
    level=logging.INFO,  # Log level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

currentDir = os.path.dirname(os.path.abspath(__file__))
with open(file=f"{os.path.join(currentDir, 'tokens.json')}", mode="r") as tokensFile:
    configTokens = json.load(tokensFile)

class MyBot(commands.Bot):
    logging = logging.getLogger('main.py')
    def __init__(self):
        self.bot = self
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all()
        )
        self.cogsToLoad = {
            'cat': cat,  # Random cat gif
            'bat': battery,  # battery info service
            'vibrate': vibrate  # vibrate service
        }

    async def on_ready(self):
        user = await self.fetch_user(476047124694433822)
        #await user.send("Bot is now online!")
        await self.change_presence(activity=discord.Game(name="v1.0"))
        # Load Cogs
        for cogName, cogClass in self.cogsToLoad.items():
            try:
                if cogName in self.cogs:
                    logging.info(f"{cogName} already loaded.")
                    continue  # Skip loading this cog if it's already loaded
                
                if cogName == 'bat':
                    asyncio.create_task(cogClass.bat_cog(self))
                else:
                    await self.add_cog(cogClass(self, configTokens, currentDir))

                logging.info(f"Successfully loaded cog: {cogName}")
            except Exception as e:
                logging.exception(f"Failed to load cog: {cogName} | ERROR: {e}")
                print(f"Failed to load cog {cogName}: {e}")

        # Sync application commands
        try:
            await self.tree.sync()
            logging.info("Slash commands synced.")
        except Exception as e:
            logging.exception(f"Error syncing commands: {e}")

    async def close(self):
        # Call the base `close()` method to handle bot shutdown
        await super().close()

if __name__ == "__main__":
    bot = MyBot()

    try:
        bot.run(configTokens['discord_token'])
    except KeyboardInterrupt:
        logging.info("\nCtrl+C detected. Shutting down gracefully...")
        asyncio.run(bot.close())
