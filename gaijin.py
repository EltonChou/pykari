import logging
from datetime import datetime as dt

import discord
from bs4 import BeautifulSoup
from EorzeaEnv import EorzeaTime, EorzeaWeather
from pymongo import MongoClient
from pytz import timezone

# client = MongoClient("localhost", 27017)
# db = client['gaijin']
# collection = db['raid']


class Gaijin(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__mongo_url = kwargs.get('mongo_url') or "localhost"
        self.__playing = discord.Game(name=kwargs.get('playing'))
        self.island_list = {
            "island1": "Eureka Anemos",
            "island2": "Eureka Pagos",
            "island3": "Eureka Pyros"
        }
        self.tw = timezone('Asia/Taipei')

    async def on_ready(self):
        await self.change_presence(game=self.__playing)

    async def on_message(self, msg):
        if not msg.author.bot:

            if msg.content.startswith('!4'):
                command = msg.content.split(' ')

                if command[1] == 'weather':
                    etl = EorzeaTime.next_weather_period_start()
                    try:
                        island = self.island_list[command[2]]
                    except KeyError as err:
                        island = None
                        print(repr(err))
                    results = []

                    if not island:
                        return
                    for time in etl:
                        from_ = dt.fromtimestamp(time, tz=self.tw).strftime("%H:%M")
                        weather = EorzeaWeather.forecast_weather(island, time).lower().replace(" ", "_")
                        icon_id = discord.utils.find(
                            lambda e: e.name == weather, msg.server.emojis).id
                        result = '<:{}:{}> {}~'.format(weather, icon_id, from_)
                        results.append(result)

                    weather_transform = "\n".join(
                        str(r) for r in results)

                    await self.send_message(msg.channel, weather_transform)
