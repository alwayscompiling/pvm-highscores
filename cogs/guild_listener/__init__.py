"""
Defines cog for guild listeners. Contains functions for various guild events.
"""

import os
import json

from nextcord.ext import commands
import nextcord

from highscores import highscores_data  # pylint: disable=import-error
from utilities.data_storage import create_highscore_skeleton  # pylint: disable=import-error
from utilities.data_storage import save_highscores_data  # pylint: disable=import-error


class GuildListener(commands.Cog, name="Guild Listener"):
    """Sets up message listener."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: nextcord.Guild):
        """Listener for Guild Join. Creates skeleton for new guild joined and saves it."""
        # turning guild id into string because json doesn't support ints as object keys.
        highscores_data[str(guild.id)] = create_highscore_skeleton()
        save_highscores_data(highscores_data)

        welcome_message: str = "Hello, I keep track of Highscores for you!"
        welcome_message += " Currently only supporting RuneScape boss highscores,"
        welcome_message += " but will be more dynamic support in future."
        welcome_message += ' For assistance on getting started, use "?register help".'

        await guild.system_channel.send(content=welcome_message)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        """Listener for Guild Remove. Removes data from highscores_data."""
        print(f"Removing data for guild {guild.name} (id {guild.id}).")
        old_data = highscores_data.pop(str(guild.id))
        save_highscores_data(highscores_data)

        if not os.path.exists("deleted_backups"):
            os.mkdir("deleted_backups")

        with open(f"deleted_backups/{guild.name}_backup.json", encoding="utf-8", mode="w") as file:
            file.write(json.dumps(old_data, indent=4))


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds function to bot"""
    bot.add_cog(GuildListener(bot))
