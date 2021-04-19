//fix counting for attachments. 
const config = require('../config.json')
const axios = require('axios')
const fs = require('fs');
const hash = require('node-image-hash')

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
            let searchHash = await axios({
                url: 'localhost:4000/graphql',
                method: 'post',
                data: {
                    query: `
                        query {
                            getPostByHash(hash: ${newHash}) {
                                id
                            }
                        }
                    `
                }
            }).data
            console.log(searchHash)
            
            /*request.head(url, (err, res, body) => {
                request(message.attachments.first().url).pipe(fs.createWriteStream(config.file_path)).on('close', (obj) => {
                    console.log(obj)
                    console.log("done")
                })
            })*/

        }
        
    }
}