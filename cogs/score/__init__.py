"""
Bot command to submit a score
"""

from nextcord.ext import commands
from utils import highscore_manage  # pylint: disable=import-error

# from utils import highscore_manage  # pylint: disable=import-error


class RegisterHighscoreChannel(commands.Cog, name="Score"):
    """Actions of bot command"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="score")
    async def score(self, ctx: commands.Context, boss: str, category: str, score):
        """A command which calls a function to submit the score to highscores. Gathers required
        information from command and passes on.
        Usage:
        ```
        ?score "Boss Name" "Category" "score"
        ```
        """
        highscore_manage.submit_score_int(boss, category, ctx.author.display_name, score)


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds functon to bot"""
    bot.add_cog(RegisterHighscoreChannel(bot))
