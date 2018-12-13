from datetime import datetime as _dt

from discord import utils as _du
from EorzeaEnv import EorzeaTime, EorzeaWeather
from pytz import timezone


class Command:

    def on_message(message):
        command = info_brew(message)[0]
        func_to_call = getattr(Command, command[1])
        return func_to_call(message)

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

        period = EorzeaTime.next_weather_period_start()

        results = []
        for time in period:
            from_ = _dt.fromtimestamp(
                time, tz=timezone('Asia/Taipei')).strftime("%H:%M")
            weather = EorzeaWeather.forecast_weather(island, time)
            emoji = get_emoji(weather, emojis)

            try:
                result = wrap_result(emoji, from_)
            except AttributeError:
                result = wrap_result(weather, from_)

            results.append(result)

        return wrap_message(results)


def info_brew(msg):
    command = msg.content.split(' ')
    server = msg.server
    emojis = msg.server.emojis
    return command, server, emojis


def _shiranai(kw):
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
    return '{} `{}~`'.format(weather, from_)
