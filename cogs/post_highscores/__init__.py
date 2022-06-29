"""
Bot command to post the highscores
"""

from nextcord.ext import commands
from highscores import highscores_config  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error
from utils import data_storage  # pylint: disable=import-error
from utils import highscore_message  # pylint: disable=import-error


class PostHighscores(commands.Cog, name="Post Highscores"):
    """Actions of bot command"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="post-scores")
    async def post_highscores(self, ctx: commands.Context):
        """
        A command which posts the highscore in the designated channel. Sends warning if no channel
        has been registered.
        Usage:
        ```
        ?post-scores
        ```
        """
        # temporarily sending config data...
        channel_id = highscores_data["channel_id"]
        print(f"Printing out highscores information in channel {channel_id}")
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            response = 'Registered Highscores channel does not exist or was never registered. \
                Register with "?register" command.'
            await ctx.send(response)
            return
        for boss in highscores_config["bosses"]:
            await highscore_message.send_highscore_message(channel, boss)

        data_storage.save_highscores_data(highscores_data)


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds functon to bot"""
    bot.add_cog(PostHighscores(bot))
