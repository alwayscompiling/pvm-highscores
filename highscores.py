"""
main file for pvm-highscores bot
"""

import os
import logging
import json
import nextcord
from nextcord.ext import commands

import config


logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

highscores_config_file = "highscores_config.json"
highscores_data_file = "highscores_data.json"


def main():
    """Main function for bot."""
    # Allows privledged intents for monitoring members joining, roles editing, and role assignments
    # These need to be enabled in the developer portal as well
    intents = nextcord.Intents.default()

    # Required in order to read messages (eg. prefix commands)
    intents.message_content = True

    # To enable the guilds priveleged intent:
    # intents.guilds = True

    # To enable the members priveleged intent:
    # intents.members = True

    # Set custom status to "Listening to ?help"
    activity = nextcord.Activity(
        type=nextcord.ActivityType.listening, name=f"{config.BOT_PREFIX}help"
    )

    bot = commands.Bot(
        commands.when_mentioned_or(config.BOT_PREFIX),
        intents=intents,
        activity=activity,
    )

    # Get the modules of all cogs whose directory structure is ./cogs/<module_name>
    for folder in os.listdir("cogs"):
        bot.load_extension(f"cogs.{folder}")

    @bot.listen()
    async def on_ready():
        """When Discord is connected"""
        assert bot.user is not None
        print(f"{bot.user.name} has connected to Discord!")

    # Run Discord bot
    bot.run(config.DISCORD_TOKEN)


def open_highscores_data():
    """Opens a highscores_data.json file if one exists, otherwise creates a skeleton of the data."""
    if (os.path.exists(highscores_data_file)):
        with open(highscores_data_file, encoding='utf-8', mode="r") as file:
            data = json.load(file)
    else:
        # create the json object
        x = {
            "channel_id": 0
        }
        data = json.dumps(x)

    return data


def open_highscores_config():
    """Opens the highscores config file as a json object and returns."""
    # Load bot config
    with open(highscores_config_file, encoding='utf-8', mode='r') as file:
        highscores_config = json.load(file)
    return highscores_config


def save_highscores_data(data):
    """Saves the highscores data into a json file."""
    with open(highscores_data_file, encoding='utf-8', mode='w') as file:
        file.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
