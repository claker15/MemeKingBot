const query = require('./query.js');
const config = require('../config.json');
const youtubeUrl = require('youtube-url');

const hashImage = require('node-image-hash');
const fetch = require('node-fetch');
const fs = require('fs');

async function onCooldown(author_id, guild_id) {
    let prevPost =  await query.getPreviousPost(author_id, guild_id);
    if (prevPost != null) {
        let prevTime = prevPost.created;
        let nowTime = new Date().getTime();
        console.log("cooldown time: " + (nowTime - prevTime) / (1000 * 60));
        if ((nowTime - prevTime) / (1000 * 60) < config.cooldown_timer) {
            return true;
        }
        return false;
    }
}

async function urlProcess(urls, author_id, guild_id) {
    console.log(urls)
    for (let i = 0; i < urls.length; i++){
        if (youtubeUrl.valid(urls[i])) {
            let id = youtubeUrl.extractId(urls[i]);
            let post =  await query.getPostByHash(id, guild_id);
            console.log(post);
            if (post.hash == null || post.hash == '') {
                let input = {
                    hash: id,
                    path: urls[i],
                    user_id: author_id,
                    guild_id: guild_id
                };
                await query.createPost(input);
            }
            else {
                  return true;       
            }     
        }
    }
    return false;
}

async function attachProcess(attachments, author_id, guild_id) {
    for (let i = 0; i < attachments.length; i++) {
        let hash = await getImageHash(attachments[i].url);
        let post =  await query.getPostByHash(hash, guild_id);
        if (post != null) {
            return true;
        }
        let path = '/' + attachments[i].name;
        if (config.environment == 'prod') {
            fs.writeFileSync(config.file_path + path, buffer, function(err) {
                if (err) {
                    console.log(err);
                }
                else {
                    console.log("File saved");
                }
            });
        } 
        let input = {
            hash: hash,
            path: config.file_path + path,
            user_id: author_id,
            guild_id: guild_id
        };
        await query.createPost(input);
        return false;
        
    }
    return true;
}

async function getImageHash(url) {
    let res = await fetch(url);
    let arrayBuffer = await res.arrayBuffer();
    let buffer = Buffer.from(arrayBuffer);
    let newHash = await hashImage.hash(buffer, 64, 'base64');
    return newHash.hash;
}

module.exports = {
    onCooldown,
    urlProcess,
    attachProcess
}