"""
Bot command to post the highscores
"""

from nextcord.ext import commands
import highscores  # pylint: disable=import-error


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
                print(boss)
                boss_name = boss["boss"]
                highscore_string = f"**{boss_name}**"
                await channel.send(highscore_string)
        else:
            response = "Highscores channel is not registered. Register with \"?register\" command."
            await ctx.send(response)


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds functon to bot"""
    bot.add_cog(PostHighscores(bot))
