const { GuildManager } = require("discord.js")
const config = require("../config.json")

module.exports = {
    name: 'crown',
    execute(client, tally) {
        var guilds = config.servers
        guilds.forEach((e) => {
            var temp = filterGuild(tally, e)
            var temp2 = temp.sort((first, second) => {
                first.value - second.value
            })
            var king = temp2[0].id
            client.guilds.fetch(e).then((guildmanager) => {
                guildmanager.members.fetch(king).then((user) => {
                    user.setNickname("Meme King of the Week")
                }).catch(console.error)
            }).catch(console.error)

        })
    }
}

function filterGuild(arr, id) {
    return arr.filter((e) => e.guild === id)
}