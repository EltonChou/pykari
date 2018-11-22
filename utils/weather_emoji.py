weather = self.ew.forecast_weather(island).lower().replace(" ", "_")
emoji_id = discord.utils.find(lambda e: e.name == weather, msg.server.emojis).id
weather_emoji = '<:{}:{}>'.format(weather, emoji_id)
