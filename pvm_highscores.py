"""
pvm_highscores discord bot
"""

import json
import logging
import discord

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


client = discord.Client()

with open("config.json", encoding='utf-8', mode='r') as file:
    config_data = json.load(file)


@client.event
async def on_ready():
    """"reports when bot logs in"""
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    """"runs when message is sent on server"""
    print("message get")
    if message.author == client.user:
        return

    if message.content.startswith('reee'):
        await message.channel.send('reee!')

client.run(config_data["token"])
