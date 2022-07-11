"""
Defines cog for on message listener.
"""

from nextcord.ext import commands
import nextcord

from highscores import submission_messages  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error


class SubmissionListener(commands.Cog, name="Message Listener"):
    """Sets up message listener."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, proof_message: nextcord.Message):
        """Listener for message creation. Adds score and attachments to submission."""
        if proof_message.author.id in submission_messages:
            message_id = submission_messages[proof_message.author.id]
            submission_message: nextcord.Message = await self.bot.get_channel(
                highscores_data["submission_channel_id"]
            ).fetch_message(message_id)

            # need check if correct user and correct channel
            if proof_message.channel.id == highscores_data["submission_channel_id"]:

                embed = submission_message.embeds[0]
                embed.add_field(name="Score", value=proof_message.content, inline=False)
                await submission_message.edit(
                    files=[await attch.to_file() for attch in proof_message.attachments],
                    embed=embed,
                )
                await proof_message.delete()


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds function to bot"""
    bot.add_cog(SubmissionListener(bot))
