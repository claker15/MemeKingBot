//fix counting for attachments. 
const config = require('../config.json')

module.exports = {
    name: 'message',
    execute(message, client, tally) {
        if (message.content.startsWith(config.prefix)) {
            var args = message.content.slice(config.prefix.length).trim().split(/ +/);
	        var command = args.shift().toLowerCase();
            client.commands.get(command).execute(message)
        }
        if ((message.attachments.array().length > 0) || message.embeds.length > 0) {
            let element = tally.find(e => e.id = message.author.id)
            if (element == undefined) {
               tally.push({guild: message.guild.id, id: message.author.id, value: 1})
            }
            else {
               element.value++
            };
        }
        
    }
}