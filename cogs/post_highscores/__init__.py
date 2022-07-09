"""
Bot command to post the highscores
"""

from nextcord.ext import commands
import nextcord

from cogs.submission.submission_views import SubmissionButton  # pylint: disable=import-error
from highscores import highscores_config  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error
from utilities.data_storage import save_highscores_data  # pylint: disable=import-error
from utilities.utils import send_highscore_message  # pylint: disable=import-error


class PostHighscores(commands.Cog, name="Post Highscores"):
    """Posts Highscores."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="post-scores")
    async def post_highscores(self, ctx: commands.Context):
        """
        A command which posts the highscore in the designated channel.
        Sends warning if no channel has been registered.
        Usage:
        ```
        ?post-scores
        ```
        """
        highscore_channel_id = highscores_data["highscore_channel_id"]
        print(f"Printing out highscores information in channel {highscore_channel_id}")
        channel = self.bot.get_channel(highscore_channel_id)

        error_response = 'Registered Highscores channel does not exist or was never registered. \n\
                Register with "?register" command.'
        assert channel is not None, await ctx.send(error_response)

        for boss in highscores_config["bosses"]:
            message: nextcord.Message = await send_highscore_message(channel, boss["boss"])
            await message.edit(view=SubmissionButton(self.bot))

        save_highscores_data(highscores_data)


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds function to bot"""
    bot.add_cog(PostHighscores(bot))
