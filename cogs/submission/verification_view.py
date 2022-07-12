"""View for verification buttons"""

import nextcord
from utilities.utils import submit_score  # pylint: disable=import-error


class VerificationView(nextcord.ui.View):
    """Defines views for verifying score submissions"""

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Approve", style=nextcord.ButtonStyle.green, custom_id="approve-button-submission"
    )
    async def approve_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):  # pylint: disable=unused-argument
        """Button for approving score submission."""
        content = interaction.message.embeds[0].to_dict()

        for field in content["fields"]:
            if field["name"] == "Boss":
                boss_name = field["value"]
            elif field["name"] == "Category":
                category = field["value"]
            elif field["name"] == "Score":
                score = field["value"]
            elif field["name"] == "User":
                user = field["value"]

        try:
            await submit_score(interaction, user, boss_name, category, score)
            await interaction.message.edit("Approved.", view=None)
        except UnboundLocalError:
            await interaction.send("Instruct user to submit with all fields.")
            await interaction.message.edit(view=None)

    @nextcord.ui.button(
        label="Deny", style=nextcord.ButtonStyle.red, custom_id="deny-button-submission"
    )
    async def deny_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):  # pylint: disable=unused-argument
        """Button for denying score submission."""
        await interaction.message.delete()
