import discord
from discord.ext import commands
import aiohttp
import asyncio, logging

class cat(commands.Cog):
    logging = logging.getLogger('main.py')
    def __init__(self, client: commands.Bot, config: dict, currentDir: str):
        self.client = client
        self.config = config
        self.currentDir = currentDir

    @commands.command(name='cat')
    async def pointer_command(self, ctx):
        if ctx.author.bot or ctx.author.id != 476047124694433822:
            return
        if ctx.author.id == 476047124694433822 or ctx.author.id == 470657587898220554:
            await ctx.send('Hello, master!')
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.thecatapi.com/v1/images/search') as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        await ctx.send(data[0]['url'])
                    else:
                        await ctx.send('Could not fetch a cat gif at the moment.')
        else:
            await ctx.send('You do not have permission to use this command.')
