import os
import discord
import asyncio
import twitter
import json
import sqlite3
import datetime
import logging

from discord.ext import commands
# from secret import DISCORD_TOKEN, CONSUMER_KEY, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,  ACCESS_TOKEN_SECRET


# set constant
LOG_FILENAME = 'log.log'
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']


logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
client = discord.Client()
bot = commands.Bot(command_prefix='!4')
api = twitter.Api(
	consumer_key=CONSUMER_KEY,
	consumer_secret=CONSUMER_SECRET,
	access_token_key=ACCESS_TOKEN,
	access_token_secret=ACCESS_TOKEN_SECRET
)

def dump_following():
	users = api.GetFriends()
	db_connect = sqlite3.connect('test.sqlite')
	cursor = db_connect.cursor()
	print("DUMPING FOLLWING-LIST NOW")
	for user in users:
		cursor.execute(
			'''REPLACE INTO following (id, name, screen_name) VALUES(?,?,?)''', 
			[user.id, user.name, user.screen_name]
		)
	db_connect.commit()
	print("DUMPING FINISHED")
	db_connect.close()


def find_circle(event):
	que = "SELECT * FROM following WHERE name LIKE '%" + \
		event + "%' ORDER BY id, screen_name"
	conn = sqlite3.connect('test.sqlite')
	conn.row_factory = sqlite3.Row
	cursor = conn.cursor()
	cursor.execute(que)
	return cursor


@client.event
async def on_message(message):
	if message.content.startswith('!4'):
		command = message.content.split(' ')
		authors = find_circle(command[1])
		if len(command) > 2:
			await client.send_message(message.channel, "You know too much.")
		else:
			authors_as_json = []
			for author in authors:
				author_as_json = {
					"id": author['id'],
					"name": author['name'],
					"screen_name": author['screen_name']
				}
				authors_as_json.append(author_as_json)
			if len(json.dumps(authors_as_json)) < 2000:
				await client.send_message(message.channel, authors_as_json)
			else:
				await client.send_message(message.channel, "Sorry, the JSON is too long to send.")
	if message.content.startswith('0d'):
		await client.send_message(message.channel, "ROGER THAT")
		dump_following()
		await client.send_message(message.channel, "DUMMPING FINISHED")


@client.event
async def on_ready():
	"""Called when the bot is ready.
	"""
	print('Logged in as {name} <{id}>'.format(
		name=client.user.name, id=client.user.id))
	print('-------------------')


if __name__ == '__main__':
	client.run(DISCORD_TOKEN)
