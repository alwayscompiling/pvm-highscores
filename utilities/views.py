"""Views used in highscores bot."""

import nextcord
from utilities.data_storage import open_message_map  # pylint: disable=import-error


class SubmissionButtonView(nextcord.ui.View):
    """Defines view for score submission."""

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Submit", style=nextcord.ButtonStyle.green, custom_id="submit")
    async def submit_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):  # pylint: disable=unused-argument
        """Button for score submission."""
        highscores_message_map = open_message_map()
        boss_name = highscores_message_map[str(interaction.message.id)]
        await interaction.channel.send(f"Submitting score for {boss_name}")
