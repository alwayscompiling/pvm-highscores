"""
main file for pvm-highscores bot
"""

import logging
import os

import nextcord
from nextcord.ext import commands

import config
from utilities.data_storage import open_highscores_config
from utilities.data_storage import open_highscores_data
from utilities.data_storage import create_message_map

logger = logging.getLogger("nextcord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


highscores_config = open_highscores_config()
highscores_data = open_highscores_data()
highscores_message_map = create_message_map(highscores_data)

submission_objects: dict = {}


def main():
    """Main function for bot."""
    # Allows privledged intents for monitoring members joining, roles editing, and role assignments
    # These need to be enabled in the developer portal as well
    intents = nextcord.Intents.default()

    # Required in order to read messages (eg. prefix commands)
    intents.message_content = True  # pylint: disable=assigning-non-slot

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


if __name__ == "__main__":
    main()
