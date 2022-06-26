from nextcord.ext import commands
import highscores  # pylint: disable=import-error


class RegisterHighscoreChannel(commands.Cog, name="Register HighScore Channel"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="register")
    async def ping(self, ctx: commands.Context):
        """A command which registers the channel command is sent in as channel to post highscores in
        Usage:
        ```
        ?register (in channel to post highscores in)
        ```
        """
        # log in console that a ping was received
        print(f"Registering {ctx.channel.id}.")
        print(bot.open_highscores_data())
        # respond to the message
        await ctx.send(f"Registered <#{ctx.channel.id}> as channel to post highscores in.")


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    bot.add_cog(RegisterHighscoreChannel(bot))
