"""Views used for submission process."""

from typing import Optional
from enum import Enum

import nextcord
from nextcord import Embed
from nextcord.ext import commands

from highscores import highscores_config  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error
from highscores import highscores_message_map  # pylint: disable=import-error
from highscores import submission_objects  # pylint: disable=import-error
from .verification_view import VerificationView


class SubmissionState(Enum):
    """Enum for which state a submission is in"""

    CATEGORY = 1
    SCORE = 2
    PROOF = 3
    NAME = 4
    SUBMIT = 5
    VERIFY = 6


def get_submission_embed(userid: int) -> nextcord.Embed:
    """Creates an embed based off of the submission state and fields filled out."""
    usersubmission: dict = submission_objects[userid]
    state: SubmissionState = usersubmission["submission_state"]

    if state is SubmissionState.CATEGORY:
        description = "Step 1: Choose your category!"
    elif state is SubmissionState.SCORE:
        description = "Step 2: Input your score!"
    elif state is SubmissionState.PROOF:
        description = "Step 3: Submit your proof!"
    elif state is SubmissionState.NAME:
        description = "Step 4 (Optional): Change name on submission! (proceed to next if skipping)"
    elif state is SubmissionState.SUBMIT:
        description = "Step 5: Submit if everything looks correct!"
    elif state is SubmissionState.VERIFY:
        description = "Review fields and accept."

    embed = Embed(title="Highscores Submission", description=description)
    embed.add_field(name="User Name", value=usersubmission["username"], inline=False)
    embed.add_field(name="Boss", value=usersubmission["boss_name"], inline=False)
    if usersubmission["category"]:
        embed.add_field(name="Category", value=usersubmission["category"], inline=False)
    if usersubmission["score"]:
        embed.add_field(name="Score", value=usersubmission["score"], inline=False)
    return embed


def category_select_options(boss_name: str) -> "list[nextcord.SelectOption]":
    """Returns list of categories for a given boss."""
    options: "list[nextcord.SelectOption]" = []
    category_list = highscores_config["tables"][boss_name]
    for category in category_list:
        options.append(nextcord.SelectOption(label=category))

    return options


############ Items used in submission process ############


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
        submission_objects[interaction.user.id]["category"] = self.values[0]
        embed = get_submission_embed(interaction.user.id)
        await interaction.message.edit(
            embed=embed,
        )


class BackButton(nextcord.ui.Button):
    """Defines view for back button."""

    def __init__(self, bot: commands.Bot):
        super().__init__(label="Back", style=nextcord.ButtonStyle.primary, custom_id="back")
        self._bot = bot

    async def callback(self, interaction: nextcord.Interaction):
        state: SubmissionState = submission_objects[interaction.user.id]["submission_state"]
        state = SubmissionState(state.value - 1)
        submission_objects[interaction.user.id]["submission_state"] = state
        embed = get_submission_embed(interaction.user.id)
        await interaction.edit(embed=embed, view=SubmissionView(self._bot, interaction.user.id))


class CancelButton(nextcord.ui.Button):
    """Deletes message to cancel interaction.."""

    def __init__(self):
        super().__init__(label="Cancel", style=nextcord.ButtonStyle.red, custom_id="cancel")

    async def callback(self, interaction: nextcord.Interaction):
        submission_objects.pop(interaction.user.id)
        await interaction.message.delete()


class NextButton(nextcord.ui.Button):
    """Defines view for next button."""

    def __init__(self, bot: commands.Bot):
        super().__init__(label="Next", style=nextcord.ButtonStyle.primary, custom_id="next")
        self._bot = bot

    async def callback(self, interaction: nextcord.Interaction):
        # check if fields have been filled out for each state
        state: SubmissionState = submission_objects[interaction.user.id]["submission_state"]
        if (
            state == SubmissionState.CATEGORY
            and not submission_objects[interaction.user.id]["category"]
        ):
            await interaction.send("Please choose a category.", ephemeral=True)
        elif (
            state == SubmissionState.SCORE and not submission_objects[interaction.user.id]["score"]
        ):
            await interaction.send("Please send a score.", ephemeral=True)
        elif state == SubmissionState.PROOF and not len(interaction.message.attachments) > 0:
            await interaction.send("Please attach picture for proof.", ephemeral=True)
        else:
            state = SubmissionState(state.value + 1)
            submission_objects[interaction.user.id]["submission_state"] = state
            embed = get_submission_embed(interaction.user.id)
            await interaction.edit(embed=embed, view=SubmissionView(self._bot, interaction.user.id))


class SubmitButton(nextcord.ui.Button):
    """Defines button to submit a user's score."""

    def __init__(self, bot: commands.Bot):
        super().__init__(label="Submit", style=nextcord.ButtonStyle.green, custom_id="submit")
        self._bot = bot

    async def callback(self, interaction: nextcord.Interaction):
        verification_channel_id = highscores_data[str(interaction.guild.id)][
            "verification_channel_id"
        ]
        channel = interaction.guild.get_channel(verification_channel_id)

        error_response = "Registered Verification channel does not exist or was never registered. \
                Contact server admins."
        assert channel is not None, await channel.send(error_response)

        submission_objects[interaction.user.id]["submission_state"] = SubmissionState.VERIFY

        embed = get_submission_embed(interaction.user.id)

        await channel.send(
            files=[await attch.to_file() for attch in interaction.message.attachments],
            view=VerificationView(),
            embed=embed,
            content=f"Submission from {interaction.user.display_name}",
        )
        await interaction.message.edit(content=f"<@{interaction.user.id}> Submitted!", view=None)
        submission_objects.pop(interaction.user.id)


############ Submission Views ############


class SubmissionCreateButton(nextcord.ui.View):
    """Defines view for score submission button."""

    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self._bot = bot

    @nextcord.ui.button(
        label="Submit", style=nextcord.ButtonStyle.primary, custom_id="submitcreate"
    )
    async def submitcreate_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):  # pylint: disable=unused-argument
        """Button for score submission."""
        guild_data = highscores_data[str(interaction.guild.id)]

        boss_name = highscores_message_map[interaction.guild.id][interaction.message.id]
        channel = interaction.guild.get_channel(guild_data["submission_channel_id"])

        # a user should only have 1 submission active at once.
        # submitting with dummy message_id until message created
        # split username on pipe.
        submission_objects[interaction.user.id] = {
            "message_id": 0,
            "submission_state": SubmissionState.CATEGORY,
            "boss_name": boss_name,
            "score": "",
            "category": "",
            "username": interaction.user.display_name.split("|")[0][
                : guild_data["username_length"]
            ],
        }

        embed = get_submission_embed(interaction.user.id)

        submission_message = await channel.send(
            f"<@{interaction.user.id}>",
            view=SubmissionView(
                self._bot,
                interaction.user.id,
            ),
            embed=embed,
        )

        # update the message_id once its created
        submission_objects[interaction.user.id]["message_id"] = submission_message.id


class SubmissionView(nextcord.ui.View):
    """Defines view submitting. Adjusts to all states."""

    def __init__(
        self,
        bot: commands.Bot,
        submission_user: int,
        *,
        timeout: Optional[float] = 180,
    ):
        super().__init__(timeout=timeout)
        self._submission_user = submission_user
        self._bot = bot
        self._state = submission_objects[self._submission_user]["submission_state"]
        self._boss_name = submission_objects[self._submission_user]["boss_name"]

        # add items depending on given state
        if self._state is SubmissionState.CATEGORY:
            self.add_item(SubmissionDropdown(bot, category_select_options(self._boss_name)))
            self.add_item(CancelButton())
            self.add_item(NextButton(self._bot))
        elif (
            self._state is SubmissionState.SCORE
            or self._state is SubmissionState.PROOF
            or self._state is SubmissionState.NAME
        ):
            self.add_item(BackButton(self._bot))
            self.add_item(NextButton(self._bot))
        elif self._state is SubmissionState.SUBMIT:
            self.add_item(BackButton(self._bot))
            self.add_item(SubmitButton(self._bot))

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return self._submission_user == interaction.user.id
