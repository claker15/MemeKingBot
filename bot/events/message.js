//fix counting for attachments. 
const config = require('../config.json')
const axios = require('axios')
const fs = require('fs');
const hash = require('node-image-hash');
const fetch = require('node-fetch')

module.exports = {
    name: 'message',
    async execute(message, client) {
        if (message.content.startsWith(config.prefix)) {
            var args = message.content.slice(config.prefix.length).trim().split(/ +/);
	        var command = args.shift().toLowerCase();
            client.commands.get(command).execute(message)
        }
        if ((message.attachments.array().length > 0) || message.embeds.length > 0) {
            console.log(message)
            let url = message.attachments.first().url
            let res = await fetch(url)
            let arrayBuffer = await res.arrayBuffer()
            let buffer = Buffer.from(arrayBuffer)
            let newHash = await hash.hash(buffer, 64, 'base64')
            let test = await axios.post('http://192.168.1.86:4000/graphql', {
                query: `query getPostByHash($hash: String){
                            getPostByHash(hash: $hash) {
                                hash
                                path
                            }
                        }`,
                variables: {
                    hash: newHash.hash
                },

            }, {headers:{'Content-Type': 'application/json'}})
            if (test.data.data.getPostByHash == null) {
                let path = '/' + message.attachments.first().name
                fs.createWriteStream(config.file_path + path).write(buffer)
                //enter data into database
                let input = {
                    hash: newHash.hash,
                    path: config.file_path + path,
                    user_id: message.author.id,
                    guild_id: message.guild.id,
                    created: new Date().toISOString().split('T')[0]
                }
                let test2 = await axios.post('http://192.168.1.86:4000/graphql', {
                    query: `mutation createPost($input: postInput) {
                                createPost(input: $input)
                    }`,
                    variables: {
                        input: input
                    }
                })
            }
        }
        
    }
}