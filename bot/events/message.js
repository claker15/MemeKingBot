//fix counting for attachments. 
const config = require('../config.json')
const axios = require('axios')
const getUrls = require('get-urls');
const query = require('../modules/query.js');
const messageUtils = require('../modules/messageParse.js');

module.exports = {
    name: 'message',
    async execute(message, client) {
        if (message.content.startsWith(config.prefix)) {
            var args = message.content.slice(config.prefix.length).trim().split(/ +/);
	        var command = args.shift().toLowerCase();
            client.commands.get(command).execute(message);
        }
        let urls = getUrls(message.content);
        if (urls.size > 0) {
            let coolDown = await messageUtils.onCooldown(message.author.id, message.guild.id);
            if (coolDown) {
                message.channel.send(`${message.author} https://cdn.discordapp.com/attachments/759174594933817365/857718366491639828/Relax.png`);
            }
            else {
                let urlExist = await messageUtils.urlProcess(Array.from(urls), message.author.id, message.guild.id);
                if (urlExist) {
                    message.channel.send(`${message.author} Cringe. Old meme,   :b:ruh https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png`);
                }
            }
            
        }
        if (message.attachments.array().length > 0) {
            let coolDown = await messageUtils.onCooldown(message.author.id, message.guild.id);
            if (coolDown) {
                message.channel.send(`${message.author} https://cdn.discordapp.com/attachments/759174594933817365/857718366491639828/Relax.png`);
            }
            else {
                let imageExists = await messageUtils.attachProcess(message.attachments.array(), message.author.id, message.guild.id);
                if (imageExists) {
                    message.channel.send(`${message.author} Cringe. Old meme,   :b:ruh https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png`);
                }
            }
            
        }
        
    }
}