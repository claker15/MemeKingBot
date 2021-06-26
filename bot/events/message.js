//fix counting for attachments. 
const config = require('../config.json')
const axios = require('axios')
const fs = require('fs');
const hash = require('node-image-hash');
const fetch = require('node-fetch');
const youtubeUrl = require('youtube-url');
const getUrls = require('get-urls');

module.exports = {
    name: 'message',
    async execute(message, client) {
        if (message.content.startsWith(config.prefix)) {
            var args = message.content.slice(config.prefix.length).trim().split(/ +/);
	        var command = args.shift().toLowerCase();
            client.commands.get(command).execute(message);
        }
        if (message.content != "") {
            let urls = getUrls(message.content);
            urls.forEach(async (url) => {
                if (youtubeUrl.valid(url)) {
                    let id = youtubeUrl.extractId(url);
                    let res = await axios.post(config.api_server_url, {
                        query: `query getPostByHash($hash: String, $guild_id: String){
                                    getPostByHash(hash: $hash, guild_id: $guild_id) {
                                        hash
                                        path
                                    }
                                }`,
                            variables: {
                                hash: id,
                                guild_id: message.guild.id
                            },
            
                        }, {headers:{'Content-Type': 'application/json'}});
                        //to-do create post using id as hash and path being url
                    if (res.data.data.getPostByHash == null) {
                        let input = {
                            hash: id,
                            path: url,
                            user_id: message.author.id,
                            guild_id: message.guild.id
                        };
                        await axios.post(config.api_server_url, {
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
            });
        }
        if ((message.attachments.array().length > 0)) {
            let res = await axios.post(config.api_server_url, {
                query: `query getPreviousPost($user_id: String, $guild_id: String){
                            getPreviousPost(user_id: $user_id, guild_id: $guild_id) {
                                created
                            }
                        }`,
                    variables: {
                        user_id: message.author.id,
                        guild_id: message.guild.id
                    },
    
                }, {headers:{'Content-Type': 'application/json'}});
            if (res.data.data.getPreviousPost != null) {
                let prevTime = res.data.data.getPreviousPost.created;
                let nowTime = new Date().getTime();
                console.log(`prevTime: ${prevTime}, nowTime: ${nowTime}`)
                console.log((nowTime - prevTime) / (1000 * 60));
                if ((nowTime - prevTime) / (1000 * 60) < config.cooldown_timer) {
                    message.channel.send(`${message.author} 'https://cdn.discordapp.com/attachments/759174594933817365/857718366491639828/Relax.png'`);
                    return;
                }
            }
            let url = message.attachments.first().url;
            res = await fetch(url);
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