"""Views used in highscores bot."""

from typing import Optional

import nextcord

from utilities.data_storage import open_message_map  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error


class SubmissionButton(nextcord.ui.View):
    """Defines view for score submission button."""

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Submit", style=nextcord.ButtonStyle.green, custom_id="submit")
    async def submit_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):  # pylint: disable=unused-argument
        """Button for score submission."""
        highscores_message_map = open_message_map()
        boss_name = highscores_message_map[str(interaction.message.id)]
        await interaction.channel.send(
            f"Submitting score for {boss_name}",
            view=SubmissionView(await self._category_select_options(boss_name)),
        )

    async def _category_select_options(self, boss_name: str) -> "list[nextcord.SelectOption]":
        options: list[nextcord.SelectOption] = []  # pylint: disable=unsubscriptable-object
        boss_dict = highscores_data[boss_name]
        for category in boss_dict["categories"].items():
            options.append(nextcord.SelectOption(label=category[0]))

        return options


class SubmissionDropdown(nextcord.ui.Select):
    """Defines dropdown menu for submission"""

    def __init__(self, options: "list[nextcord.SelectOption]"):
        super().__init__(
            placeholder="Choose submission category.", min_values=1, max_values=1, options=options
        )

        def callback(self, interaction: nextcord.Interaction):
            pass


class SubmissionView(nextcord.ui.View):
    """Defines entire submission process view"""

    def __init__(
        self,
        # button_view: SubmissionButtonView.submit_button,
        options: "list[nextcord.SelectOption]",
        *,
        timeout: Optional[float] = 180,
    ):
        super().__init__(timeout=timeout)
        self.add_item(SubmissionDropdown(options))
        # self._button_view = button_view

    # async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
    #     return self._button_view.interaction.user == interaction.user  # unsure if works
