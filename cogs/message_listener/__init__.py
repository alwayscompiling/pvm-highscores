"""
Defines cog for on message listener.
"""

import re

from nextcord.ext import commands
import nextcord

from cogs.submission.submission_views import SubmissionState  # pylint: disable=import-error
from cogs.submission.submission_views import get_submission_embed  # pylint: disable=import-error
from highscores import highscores_config  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error
from highscores import submission_objects  # pylint: disable=import-error


class SubmissionListener(commands.Cog, name="Message Listener"):
    """Sets up message listener."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        """Listener for message creation. Adds score and attachments to submission."""
        if message.author.id in submission_objects:
            message_id = submission_objects[message.author.id]["message_id"]
            submission_message: nextcord.Message = await self.bot.get_channel(
                highscores_data["submission_channel_id"]
            ).fetch_message(message_id)

            # need check if correct user and correct channel
            if message.channel.id == highscores_data["submission_channel_id"]:
                state = submission_objects[message.author.id]["submission_state"]
                if state == SubmissionState.SCORE and message.content:

                    # check with regex if score matches correctly
                    is_time_record = highscores_config["categories"][
                        submission_objects[message.author.id]["category"]
                    ]["is_time_record"]

                    time_regex = re.search(
                        "([0-9]{2}:)?[0-9]{2}(\.[0-9])?",  # pylint: disable=anomalous-backslash-in-string
                        message.content,
                    )
                    int_regex = re.search("[0-9]+", message.content)
                    if time_regex is None and is_time_record:
                        embed = submission_message.embeds[0]
                        embed.add_field(
                            name="Error",
                            value="Time record must follow format MM:SS.ms or SS.ms or SS.",
                        )
                    elif int_regex is None and not is_time_record:
                        embed = submission_message.embeds[0]
                        embed.add_field(name="Error", value="Number record must only be number.")
                    else:
                        submission_objects[message.author.id]["score"] = message.content
                        embed = get_submission_embed(message.author.id)

                    await submission_message.edit(
                        embed=embed,
                    )
                elif state == SubmissionState.PROOF and len(message.attachments) > 0:
                    await submission_message.edit(
                        files=[await attch.to_file() for attch in message.attachments],
                    )
                elif state == SubmissionState.NAME and message.content:
                    submission_objects[message.author.id]["username"] = message.content[:12]
                    embed = get_submission_embed(message.author.id)
                    await submission_message.edit(
                        embed=embed,
                    )

                await message.delete()


# This function will be called when this extension is loaded.
# It is necessary to add these functions to the bot.
def setup(bot: commands.Bot):
    """Adds function to bot"""
    bot.add_cog(SubmissionListener(bot))
