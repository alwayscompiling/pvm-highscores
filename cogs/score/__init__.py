"""
Bot command to submit a score
"""

from nextcord.ext import commands

from highscores import highscores_data  # pylint: disable=import-error
from .verification_view import VerificationView


class Score(commands.Cog, name="Score"):
    """Submits a score."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the cog is loaded"""
        self.bot.add_view(VerificationView())

    @commands.command(name="score")
    async def score(self, ctx: commands.Context, boss_name: str, category: str, score: str):
        """A command which calls a function to submit the score to highscores.
        Gathers required information from command and passes on.
        Usage:
        ```
        ?score "Boss Name" "Category" "score"
        This command still works if you prefer to use it over the ui.
        ```
        """
        guild_data = highscores_data[ctx.guild.id]
        verification_channel_id = guild_data["verification_channel_id"]
        channel = ctx.guild.get_channel(verification_channel_id)

        error_response = "Registered Verification channel does not exist or was never registered."
        error_response += "Contact server admins."
        assert channel is not None, await ctx.send(error_response)

        verification_string = f"{ctx.author.display_name}:{boss_name}:{category}:{score}"

        await channel.send(
            content=verification_string,
            files=[await attch.to_file() for attch in ctx.message.attachments],
            view=VerificationView(),
        )


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds function to bot"""
    bot.add_cog(Score(bot))
