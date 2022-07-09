"""
Cog for creating submission process.
"""

from nextcord.ext import commands

from .submission_views import SubmissionButton


class SubmissionCog(commands.Cog, name="Submission Cog"):
    """Constructs submission method."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when cog is loaded"""
        self.bot.add_view(SubmissionButton(self.bot))


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds function to bot"""
    bot.add_cog(SubmissionCog(bot))
