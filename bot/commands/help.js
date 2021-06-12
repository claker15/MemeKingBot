const Discord = require("discord.js");

const embedMessage = new Discord.MessageEmbed()
    .setTitle("MemeKingBot")
    .setURL("https://github.com/claker15/MemeKingBot")
    .setDescription("This is a bot that will crown a meme king every week. The king is the one who posts the most unique memes that week")
    .addFields(
        {name: '!rankings', value: '!WIP! Show rankings of king candidates.'},
        {name: 'The crowning', value: 'Automatically ccurs at 12:00AM Monday'},
        {name: '!help', value: 'Shows this message'},
    )

module.exports = {
    name: "help",
    description: "Prints commands",
    execute(message, args) {
        message.channel.send(embedMessage);
    }
}