const { GuildManager, DiscordAPIError } = require("discord.js")
const config = require("../config.json")

module.exports = {
    name: 'crown',
    async execute(client) {
        /*var guilds = config.servers
        guilds.forEach((e) => {
            let king = await axios.post('http://192.168.1.86:4000/graphql', {
                    query: `query getKing($guild_id: String) {
                                getKing(guild_id: $guild_id){
                                    user_id
                                }
                    }`,
                    variables: {
                        guild_id: e.id
                    }
            })
            let user = await e.members.fetch(king.data.data.getKing.user_id)
            let message = new Discord.Message().content(`${user.nickname} is the meme king of the week`).pin
            e.channels.cache.find(i => i.name.toLowerCase() === 'announcements').send(message)
        })*/
    }
}
