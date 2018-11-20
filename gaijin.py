import discord
import logging
from pymongo import MongoClient
from bs4 import BeautifulSoup
from EorzeaEnv import EorzeaWeather

# client = MongoClient("localhost", 27017)
# db = client['gaijin']
# collection = db['raid']


class Gaijin(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__mongo_url = kwargs.get('mongo_url') or "localhost"
        self.__playing = discord.Game(name=kwargs.get('playing'))
        self.ew = EorzeaWeather.EorzeaWeather()

    async def on_ready(self):
        await self.change_presence(game=self.__playing)

    async def on_message(self, msg):
        if not msg.author.bot:
            if msg.content.startswith('!4'):
                command = msg.content.split(' ')
                if command[1] == 'weather':
                    if command[2] == 'island3':
                        weather = self.ew.forecast_weather("Eureka Pyros").lower().replace(" ","_")
                        emoji_id = discord.utils.find(lambda e: e.name == weather, msg.server.emojis).id
                        weather_emoji = '<:{}:{}>'.format(self.ew.forecast_weather("Eureka Pyros").lower().replace(" ","_"), emoji_id)
                        await self.send_message(msg.channel, weather_emoji)
                    if command[2] == 'island2':
                        weather = self.ew.forecast_weather("Eureka Pagos").lower().replace(" ","_")
                        emoji_id = discord.utils.find(lambda e: e.name == weather, msg.server.emojis).id
                        weather_emoji = '<:{}:{}>'.format(self.ew.forecast_weather("Eureka Pyros").lower().replace(" ","_"), emoji_id)
                        await self.send_message(msg.channel, weather_emoji)
                    if command[2] == 'island1':
                        weather = self.ew.forecast_weather("Eureka Anemos").lower().replace(" ","_")
                        emoji_id = discord.utils.find(lambda e: e.name == weather, msg.server.emojis).id
                        weather_emoji = '<:{}:{}>'.format(self.ew.forecast_weather("Eureka Pyros").lower().replace(" ","_"), emoji_id)
                        await self.send_message(msg.channel, weather_emoji)
