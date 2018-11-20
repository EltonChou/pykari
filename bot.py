import os
import logging
from gaijin import Gaijin

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
GAIJIN_DEBUG = os.getenv('GAIJIN_DEBUG') or 0
GAME = os.getenv('GAIJIN_GAME', 'アウラの尻尾')

if GAIJIN_DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

bot = Gaijin(playing=GAME)

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)