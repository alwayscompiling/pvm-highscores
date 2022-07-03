"""
Help command
"""

from nextcord.ext import commands

from .help_command import NewHelpCommand


class HelpCog(commands.Cog):
    """Help Command"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = NewHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


# setup functions for bot
def setup(bot: commands.Bot):
    """Adds functon to bot"""
    bot.add_cog(HelpCog(bot))
