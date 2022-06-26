"""
Bot command to register the highscores channel
"""

from nextcord.ext import commands
import highscores  # pylint: disable=import-error
from utils import data_storage  # pylint: disable=import-error


class RegisterHighscoreChannel(commands.Cog, name="Register HighScore Channel"):
    """Actions of bot command"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="register")
    async def register_highscores(self, ctx: commands.Context):
        """A command which registers the channel command is sent in as channel to post highscores in
        Usage:
        ```
        ?register (in channel to post highscores in)
        ```
        """
        print(f"Registering {ctx.channel.id}.")
        # respond to the message
        await ctx.send(f"Registered <#{ctx.channel.id}> as channel to post highscores in.")
        highscores.highscores_data["channel_id"] = ctx.channel.id
        data_storage.save_highscores_data(highscores.highscores_data)


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds functon to bot"""
    bot.add_cog(RegisterHighscoreChannel(bot))