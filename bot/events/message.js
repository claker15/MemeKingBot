//fix counting for attachments. 
const config = require('../config.json')
const axios = require('axios')
const fs = require('fs');
const hash = require('node-image-hash');
const { resolve } = require('path');

module.exports = {
    name: 'message',
    async execute(message, client) {
        if (message.content.startsWith(config.prefix)) {
            var args = message.content.slice(config.prefix.length).trim().split(/ +/);
	        var command = args.shift().toLowerCase();
            client.commands.get(command).execute(message)
        }
        if ((message.attachments.array().length > 0) || message.embeds.length > 0) {
            let res = await axios.get(message.attachments.first().url, { responceType: 'arraybuffer'})
            let buffer = Buffer.from(res.data, "utf-8")
            let newHash = await hash.hash(buffer)
            console.log(newHash)
            let test = await axios.post('http://192.168.1.86:4000/graphql', {
                query: `query{
                            getPostByHash($hash: String!) {
                                hash
                                path
                            }
                        }`,
                variables: {
                    hash: newHash.hash
                },

            }, {headers:{'Content-Type': 'application/json'}}).then(res => {
                resolve(res)
            }).catch(err => {
                reject(err)
            })
            
            
            
            /*request.head(url, (err, res, body) => {
                request(message.attachments.first().url).pipe(fs.createWriteStream(config.file_path)).on('close', (obj) => {
                    console.log(obj)
                    console.log("done")
                })
            })*/

        }
        
    }
}