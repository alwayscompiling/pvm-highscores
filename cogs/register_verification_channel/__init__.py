"""
Bot command to register the verification channel
"""

from nextcord.ext import commands
from highscores import highscores_data  # pylint: disable=import-error
from utilities.data_storage import save_highscores_data  # pylint: disable=import-error


class RegisterVerificationChannel(commands.Cog, name="Register Verify Channel"):
    """Registers Verification channel"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="register-verify")
    async def register_highscores(self, ctx: commands.Context):
        """A command which registers current channel as channel to post verifications in.
        Usage:
        ```
        ?register-verify (in channel to post highscores in)
        ```
        """
        print(f"Registering {ctx.channel.id} for verification.")
        # respond to the message
        await ctx.send(f"Registered <#{ctx.channel.id}> as channel to post verifications in.")
        highscores_data["verification_channel_id"] = ctx.channel.id
        save_highscores_data(highscores_data)


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds functon to bot"""
    bot.add_cog(RegisterVerificationChannel(bot))
