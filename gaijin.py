import asyncio
import logging

import discord
from bs4 import BeautifulSoup
from pymongo import MongoClient

from utils.command import Command

# client = MongoClient("localhost", 27017)
# db = client['gaijin']
# collection = db['raid']

log = logging.getLogger('discord')


class Gaijin(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_url = kwargs.get('mongo_url') or "localhost"
        self.playing = discord.Game(name=kwargs.get('playing'))
        self.prefix = kwargs.get('prefix')

    async def on_ready(self):
        await self.change_presence(game=self.playing)

    async def on_message(self, message):
        if not message.author.bot:

            if message.content.startswith(self.prefix):
                embed = Command.on_message(message)

                await self.send_message(message.channel, embed=embed)
