import json
import discord

client = discord.Client()

with open("config.json") as file:
    config_data = json.load(file)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    print("message get")
    if message.author == client.user:
        return

    if message.content.startswith('reee'):
        await message.channel.send('reee!')

client.run(config_data["token"])
