const config = require("../config.json");
const axios = require('axios');
const Discord = require('discord.js')

module.exports = {
    name: "crowns",
    description: "Leaderboard of coronations",
    async execute(message, args) {
        
        let res = await axios.post(config.api_server_url, {
            query: `query getCrowns($guild_id: String){
                        getCrowns(guild_id: $guild_id) {
                            user_id,
                            crowns
                        }
                    }`,
            variables: {
                guild_id: message.guild.id
            },

        }, {headers:{'Content-Type': 'application/json'}});

        let usersids = res.data.data.getCrowns;

        const messageEmbed = new Discord.MessageEmbed();


        for await (let result of usersids) {
            message.guild.members.fetch(result.user_id).then((user) => {
                messageEmbed
                    .setColor('#0099ff')
                    .setTitle('Coronation Leaderboard 👑')
                    .addFields(
                        { name: user.displayName, value: result.crowns}
                    )
        })}
        message.channel.send(rankMessage);
    }
}