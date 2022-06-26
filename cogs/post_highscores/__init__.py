"""
Bot command to post the highscores
"""

from nextcord.ext import commands
import highscores  # pylint: disable=import-error
from utils import data_storage  # pylint: disable=import-error
from utils import message_formatter  # pylint: disable=import-error


class PostHighscores(commands.Cog, name="Post Highscores"):
    """Actions of bot command"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="post-scores")
    async def post_highscores(self, ctx: commands.Context):
        """A command which posts the highscore in the designated channel. Sends warning if no channel has been registered.
        Usage:
        ```
        ?post-scores
        ```
        """
        # temporarily sending config data...
        channel_id = highscores.highscores_data["channel_id"]
        if (channel_id != -1):
            print(
                f"Printing out highscores information in channel {channel_id}")
            channel = self.bot.get_channel(channel_id)
            for boss in highscores.highscores_config["bosses"]:
                highscore_string = message_formatter.format_boss_highscore(
                    boss)
                message = await channel.send(highscore_string)
                message_id = message.id

                # check if there is a dict for the boss in the highscores data
                if not boss["boss"] in highscores.highscores_data:
                    highscores.highscores_data[boss["boss"]] = {}

                highscores.highscores_data[boss["boss"]
                                           ]["message_id"] = message_id
        else:
            response = "Highscores channel is not registered. Register with \"?register\" command."
            await ctx.send(response)

        data_storage.save_highscores_data(highscores.highscores_data)


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds functon to bot"""
    bot.add_cog(PostHighscores(bot))
