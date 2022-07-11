"""Views used for submission process."""

from typing import Optional

import nextcord
from nextcord.ext import commands

from utilities.data_storage import open_message_map  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error
from highscores import submission_messages  # pylint: disable=import-error
from .verification_view import VerificationView


class SubmissionButton(nextcord.ui.View):
    """Defines view for score submission button."""

    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self._bot = bot

    @nextcord.ui.button(label="Submit", style=nextcord.ButtonStyle.primary, custom_id="submit")
    async def submit_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):  # pylint: disable=unused-argument
        """Button for score submission."""
        highscores_message_map = open_message_map()
        boss_name = highscores_message_map[str(interaction.message.id)]
        embed = nextcord.Embed(title="Highscores Submission")
        embed.add_field(name="Boss", value=boss_name, inline=False)
        embed.add_field(name="User", value=interaction.user.display_name, inline=False)
        channel = self._bot.get_channel(highscores_data["submission_channel_id"])
        submission_message = await channel.send(
            f"<@{interaction.user.id}>",
            view=SubmissionDropdownView(
                self._bot, interaction, await self._category_select_options(boss_name)
            ),
            embed=embed,
        )

        # a user should only have 1 submission active at once.
        submission_messages[interaction.user.id] = submission_message.id

    async def _category_select_options(self, boss_name: str) -> "list[nextcord.SelectOption]":
        options: list[nextcord.SelectOption] = []  # pylint: disable=unsubscriptable-object
        boss_dict = highscores_data[boss_name]
        for category in boss_dict["categories"].items():
            options.append(nextcord.SelectOption(label=category[0]))

        return options


class SubmissionDropdown(nextcord.ui.Select):
    """Defines dropdown menu for submission"""

    def __init__(
        self,
        bot: commands.Bot,
        options: "list[nextcord.SelectOption]",
    ):
        super().__init__(
            placeholder="Choose submission category.", min_values=1, max_values=1, options=options
        )
        self._bot = bot

    async def callback(self, interaction: nextcord.Interaction):
        embed = interaction.message.embeds[0]
        embed.add_field(name="Category", value=self.values[0], inline=False)
        await interaction.message.edit(
            embed=embed,
        )


class SubmissionDropdownView(nextcord.ui.View):
    """Defines submission dropdown process view"""

    def __init__(
        self,
        bot: commands.Bot,
        prev_interaction: nextcord.Interaction,
        options: "list[nextcord.SelectOption]",
        *,
        timeout: Optional[float] = 180,
    ):
        super().__init__(timeout=timeout)
        self.add_item(SubmissionDropdown(bot, options))
        self._prev_interaction = prev_interaction
        self.bot = bot

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return self._prev_interaction.user == interaction.user

    @nextcord.ui.button(
        label="Submit Score", style=nextcord.ButtonStyle.green, custom_id="submit-score"
    )
    async def submit_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):  # pylint: disable=unused-argument
        """Defines button to submit a user's score."""
        verification_channel_id = highscores_data["verification_channel_id"]
        channel = self.bot.get_channel(verification_channel_id)

        error_response = "Registered Verification channel does not exist or was never registered. \
                Contact server admins."
        assert channel is not None, await channel.send(error_response)

        await channel.send(
            files=[await attch.to_file() for attch in interaction.message.attachments],
            view=VerificationView(),
            embed=interaction.message.embeds[0],
        )
        await interaction.message.edit(content=f"<@{interaction.user.id}> Submitted!", view=None)
        submission_messages.pop(interaction.user.id)

    @nextcord.ui.button(
        label="Cancel", style=nextcord.ButtonStyle.red, custom_id="cancel-submission"
    )
    async def cancel_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):  # pylint: disable=unused-argument
        """Deletes message to cancel interaction."""
        submission_messages.pop(interaction.user.id)
        await interaction.message.delete()
