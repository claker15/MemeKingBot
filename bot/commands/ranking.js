const config = require("../config.json");
const axios = require('axios');
const Discord = require('discord.js')

module.exports = {
    name: "ranking",
    description: "Prints current ranking for week",
    async execute(message, args) {
        
        let test = await axios.post(config.api_server_url, {
            query: `query getRanking($guild_id: String){
                        getRanking(guild_id: $guild_id) {
                            user_id,
                            count
                        }
                    }`,
            variables: {
                guild_id: message.guild.id
            },

        }, {headers:{'Content-Type': 'application/json'}});
        let usersids = test.data.data.getRanking;
        let rankMessage = new Discord.MessageEmbed().setTitle("Current Meme King Rankings");
        for await (let result of usersids) {
            message.guild.members.fetch(result.user_id).then((user) => {
                rankMessage.addField(user.displayName, result.count);
            })
        }
        message.channel.send(rankMessage);
    }
}