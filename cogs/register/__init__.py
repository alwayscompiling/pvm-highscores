"""
Bot command for registering various channels to the bot.
"""

from nextcord import Embed
from nextcord.ext import commands

from highscores import highscores_data  # pylint: disable=import-error
from utilities.data_storage import save_highscores_data  # pylint: disable=import-error


class RegisterVerificationChannel(commands.Cog, name="Register"):
    """Bot command for registering various channels to the bot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="register")
    @commands.has_permissions(administrator=True)
    async def register_highscores(self, ctx: commands.Context, registration_type: str):
        """A command which registers current channel as for various uses.
        Usage:
        ```
        ?register verify (Use in channel you want to verify submissions in.)
        ?register highscore (Use in channel you want to show highscore messages in.)
        ?register submission (Use in channel you want submission messages to be send it.)
        ?register help (Shows help message.)
        ```
        """
        # respond to the message
        channel_id = ctx.channel.id
        guild_data = highscores_data[ctx.guild.id]

        if registration_type == "verify":
            await ctx.send(f"Registered <#{channel_id}> as channel to post verifications in.")
            guild_data["verification_channel_id"] = channel_id
        elif registration_type == "highscore":
            await ctx.send(f"Registered <#{channel_id}> as channel to post highscores in.")
            guild_data["highscore_channel_id"] = channel_id
        elif registration_type == "submission":
            await ctx.send(f"Registered <#{channel_id}> as channel to post submissions in.")
            guild_data["submission_channel_id"] = channel_id
        else:
            embed = Embed(
                title="Register command help", description="How to use the register command."
            )
            embed.add_field(
                name="?register verify", value="Use in channel you want to verify submissions in."
            )
            embed.add_field(
                name="?register highscore",
                value="Use in channel you want to show highscore messages in.",
            )
            embed.add_field(
                name="?register submission",
                value="Use in channel you want submission messages to be send it.",
            )
            embed.add_field(name="?register help", value="Use to show this message.")
            await ctx.reply(embed=embed)

        save_highscores_data(highscores_data)


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds function to bot"""
    bot.add_cog(RegisterVerificationChannel(bot))
