from datetime import datetime as _dt

from discord.embeds import Embed
from discord import utils as _du
from EorzeaEnv import EorzeaTime, EorzeaWeather
from pytz import timezone


class Command():

    @staticmethod
    def on_message(message):
        command = info_brew(message)[0]
        func_to_call = getattr(Command, command[1])
        return func_to_call(message)
        
    @staticmethod
    def weather(message):
        command, server, emojis = info_brew(message)
        island_list = {
            "island1": "Eureka Anemos",
            "island2": "Eureka Pagos",
            "island3": "Eureka Pyros"
        }

        island = island_list.get(command[2])

        if not island:
            return _shiranai()

        period = EorzeaTime.next_weather_period_start(6)

        eb = Embed(colour=0x50e3c2)
        eb.set_author(name=island, icon_url="https://i.imgur.com/BXfEnpu.png")
        eb.set_thumbnail(url="https://i.imgur.com/RCqN64h.png")
        for time in period:
            from_ = _dt.fromtimestamp(
                time, tz=timezone('Asia/Taipei')).strftime("%H:%M (%z)~")
            weather = EorzeaWeather.forecast_weather(island, time)

            try:
                emoji = get_emoji(weather, emojis)
                eb.add_field(name=weather + emoji, value="`{}`".format(from_), inline=True)
            except (AttributeError, TypeError):
                eb.add_field(name=weather, value="`{}`".format(from_), inline=True)

        eb.fields[0].value = "Current"
        return eb


def info_brew(msg):
    command = msg.content.split(' ')
    server = msg.server
    try:
        emojis = msg.server.emojis
    except AttributeError:
        emojis = None
    return command, server, emojis


def _shiranai():
    return "知らないですね:thinking:"


def wrap_message(results):
    return "\n".join(
        str(r) for r in results
    )


def get_emoji(name, emojis):
    name = name.lower().replace(" ", "_")
    id = _du.find(lambda e: e.name == name, emojis).id
    return '<:{}:{}>'.format(name, id)


def wrap_result(weather, from_):
    return '{} `{}`'.format(weather, from_)
