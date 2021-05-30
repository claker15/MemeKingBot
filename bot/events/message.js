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
            client.commands.get(command).execute(message);
        }
        if ((message.attachments.array().length > 0)) {
            console.log(message.guild.id)
            let url = message.attachments.first().url;
            let res = await fetch(url);
            let arrayBuffer = await res.arrayBuffer();
            let buffer = Buffer.from(arrayBuffer);
            let newHash = await hash.hash(buffer, 64, 'base64');
            let test = await axios.post(config.api_server_url, {
                query: `query getPostByHash($hash: String, $guild_id: String){
                            getPostByHash(hash: $hash, guild_id: $guild_id) {
                                hash
                                path
                            }
                        }`,
                variables: {
                    hash: newHash.hash,
                    guild_id: message.guild.id
                },

            }, {headers:{'Content-Type': 'application/json'}});
            console.log(test.data.data)
            if (test.data.data.getPostByHash == null) {
                let path = '/' + message.attachments.first().name;
                fs.writeFileSync(config.file_path + path, buffer, function(err) {

                    if (err) {
                        console.log(err);
                    }
                    else {
                        console.log("File saved");
                    }
                });
                //enter data into database;
                let input = {
                    hash: newHash.hash,
                    path: config.file_path + path,
                    user_id: message.author.id,
                    guild_id: message.guild.id,
                    created: new Date().toISOString().split('T')[0]
                };
                let test2 = await axios.post(config.api_server_url, {
                    query: `mutation createPost($input: postInput) {
                                createPost(input: $input)
                    }`,
                    variables: {
                        input: input
                    }
                });
            }
            else {
                message.channel.send(`${message.author} Cringe. Old meme,   :b:ruh https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png`);
            }
        }
        
    }
}