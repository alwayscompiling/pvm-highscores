"""View for verification buttons"""

import nextcord
from utilities.utils import submit_score  # pylint: disable=import-error


class VerificationView(nextcord.ui.View):
    """Defines views for verifying score submissions"""

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Approve", style=nextcord.ButtonStyle.green, custom_id="approve")
    async def approve_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Button for approving score submission."""
        await interaction.response.send_message("Approved")
        content = interaction.message.content.split(":")
        user = content[0]
        boss_name = content[1]
        category = content[2]
        score = content[3]

        await submit_score(interaction, user, boss_name, category, score)

    @nextcord.ui.button(label="Deny", style=nextcord.ButtonStyle.red, custom_id="deny")
    async def deny_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Button for denying score submission."""
        await interaction.response.send_message("Denied")
