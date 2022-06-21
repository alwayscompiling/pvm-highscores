const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Pings caller!'),
    async execute(interaction) {
        await interaction.reply(`Ping! <@${interaction.user.id}>`);
    },
};