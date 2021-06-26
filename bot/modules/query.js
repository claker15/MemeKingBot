const axios = require('axios');
const config = require('../config.json');


async function getPostByHash(hash, guild_id) {
    let res = await axios.post(config.api_server_url, {
        query: `query getPostByHash($hash: String, $guild_id: String){
                    getPostByHash(hash: $hash, guild_id: $guild_id) {
                        hash
                        path
                    }
                }`,
            variables: {
                hash: hash,
                guild_id: guild_id
            },

        }, {headers:{'Content-Type': 'application/json'}});
    return res.data.data.getPostByHash;
}

async function createPost(input) {
    let res = await axios.post(config.api_server_url, {
        query: `mutation createPost($input: postInput) {
                    createPost(input: $input)
        }`,
        variables: {
            input: input
        }
    }, {headers:{'Content-Type': 'application/json'}});
    return res.data.data.createPost;
}

async function getPreviousPost(user_id, guild_id) {
    let res = await axios.post(config.api_server_url, {
        query: `query getPreviousPost($user_id: String, $guild_id: String){
                    getPreviousPost(user_id: $user_id, guild_id: $guild_id) {
                        created
                    }
                }`,
            variables: {
                user_id: user_id,
                guild_id: guild_id
            },

        }, {headers:{'Content-Type': 'application/json'}});
    return res.data.data.getPreviousPost;
}

module.exports = {
    getPostByHash,
    createPost,
    getPreviousPost
}