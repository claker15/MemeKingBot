const config = require("../config.json");
const axios = require('axios');
const Discord = require('discord.js')

module.exports = {
    name: 'crown',
    execute(client) {
        var guilds = config.servers;
        var currGuild;
        var king;
        guilds.forEach((e, index) => {
            client.guilds.fetch(e).then((guild) => {
                currGuild = guild;
                axios.post(config.api_server_url, {
                    query: `query getKing($guild_id: String) {
                                getKing(guild_id: $guild_id){
                                    user_id
                                }
                    }`,
                    variables: {
                        guild_id: currGuild.id
                    }
            }).then((res) => {
                king = res.data.data.getKing.user_id
                currGuild.members.fetch(king).then((user) => {
                    let general = currGuild.channels.cache.find(channel => channel.name == config.channel_name[index]);
                    general.send(`${user.displayName} is the meme king of the week`);
                }); 
            });
            }).catch((err) => console.log(err));
        });
    }
}
