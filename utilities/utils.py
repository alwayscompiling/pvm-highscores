"""
Contains various utlity functions for highscores bot
"""

import nextcord
from highscores import highscores_config  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error
from highscores import highscores_message_map  # pylint: disable=import-error
from utilities.data_storage import save_highscores_data  # pylint: disable=import-error


def format_highscore_message(boss_name: str, guild_data: dict):
    """
    returns a formatted string for a boss's highscore
    @param boss: the dictionary object for the boss
    @param guild_data: the guild's highscore data
    @return the formatted string
    """
    ret_string = f"**{boss_name}**\n```"
    boss_data = guild_data["tables"][boss_name]

    # Gather all categories and add to string
    for key, value in boss_data["categories"].items():
        ret_string += f"{key}".ljust(26, " ")
    ret_string += "\n"

    highscore_size = highscores_config["highscore_size"]

    # list rankings in a single line. Start with first place for each category and then continue
    for i in range(highscore_size):
        for key, value in boss_data["categories"].items():
            if len(value) > i:
                score_pair = value[i]

                # pad username to max length.
                username: str = score_pair[0].ljust(guild_data["username_length"], " ")
                score: str = str(score_pair[1])

                if highscores_config["categories"][key]["is_time_record"]:
                    # pad score to correct length
                    # MM:SS.ms is 7 characters long
                    score = score.ljust(7, " ")

                line_str = f"{i+1}: {username} - "
                ret_string += line_str + score.rjust(26 - len(line_str) - 1) + " "
            else:
                ret_string += f"{i+1}: submit your score".ljust(26, " ")
        ret_string += "\n"

    return ret_string + "```"


async def send_highscore_message(
    channel: nextcord.TextChannel, boss_name: str, guild_data: dict
) -> nextcord.Message:
    """
    Function takes care of checking if a message exists for a boss, then
    creating and sending/editing the message
    @param channel: the channel to send the message in/search for message id
    @param boss: the boss to send the message about
    @param guild_data: the guild's highscore data
    @return: The nextcord message
    """
    highscore_string = format_highscore_message(boss_name, guild_data)

    message_id = guild_data["tables"][boss_name]["message_id"]
    try:
        message: nextcord.Message = await channel.fetch_message(message_id)
        await message.edit(content=highscore_string)
    except nextcord.NotFound:
        # message doesn't exist.
        message: nextcord.Message = await channel.send(highscore_string)
        message_id = message.id
        guild_data["tables"][boss_name]["message_id"] = message_id
        # save message -> boss_name in message_map
        # get guild id from channel
        # channel should come from the guild that is requesting this highscores message anyways.
        highscores_message_map[str(channel.guild.id)][message_id] = boss_name

    return message


async def submit_score(
    interaction: nextcord.Interaction, user: str, boss_name: str, category: str, score: str
):
    """
    Adds a score to the high scores and sorts. Removes a score if larger than size limit.
    @param boss: the boss to add score to
    @param category: the category to add score to
    @param user: user who submitted score
    @param score: score to add
    """

    boss_category_config = highscores_config["categories"][category]
    guild_data = highscores_data[str(interaction.guild.id)]

    # create score tuple for either time or int
    # define sort index
    if boss_category_config["is_time_record"]:
        if score.find(":") == -1:
            score_seconds = float(score)
        else:
            minutes = score.split(":")[0]
            seconds = score.split(":")[1]
            score_seconds = int(minutes) * 60 + float(seconds)
        score_tuple = (user, score, score_seconds)
        sort_index = 2

    else:
        score_tuple = (user, int(score))
        sort_index = 1

    scores: "list[tuple]" = guild_data["tables"][boss_name]["categories"][category]

    # if user is in an existing tuple, delete it.
    users_scores: "list[tuple]" = [score_tuple]
    for tup in scores:
        if user == tup[0]:
            # Add tup to users_scores, remove from scores
            users_scores.append(tup)

    # sort users_scores
    users_scores.sort(
        key=lambda x: x[sort_index],
        reverse=not boss_category_config["ascending"],
    )

    for index, tup in enumerate(users_scores):
        if index == 0:
            # first score is the best score.
            if tup not in scores:
                scores.append(tup)
        else:
            # discard all other scores from scores list.
            if tup in scores:
                scores.remove(tup)

    # sort scores.
    scores.sort(
        key=lambda x: x[sort_index],
        reverse=not boss_category_config["ascending"],
    )

    # enforce highscore size
    while len(scores) > highscores_config["highscore_size"]:
        scores.pop()
    guild_data["tables"][boss_name]["categories"][category] = scores

    # edit message
    highscore_channel_id = guild_data["highscore_channel_id"]
    print(f"Editting message {highscore_channel_id}")
    channel = interaction.guild.get_channel(highscore_channel_id)

    error_response = "Registered Highscores channel does not exist or was never registered."
    error_response += 'Register with "?register" command.'
    assert channel is not None, await interaction.send(error_response, ephemeral=True)

    await send_highscore_message(channel, boss_name, guild_data)

    # save data
    highscores_data[str(interaction.guild.id)] = guild_data
    save_highscores_data(highscores_data)
