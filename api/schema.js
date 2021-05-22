const graphql = require('graphql')
var { graphqlHTTP, GraphQLObjectType, GraphQLString, GraphQLSchema, GraphQLList, GraphQLInt, GraphQLD, GraphQLInputObjectType} = graphql;
const mysql = require('mysql');


let conn = mysql.createConnection({
    host: 'localhost',
    user: 'api',
    password: 'apipassword',
    database: 'discord_bot'
})
const postInput = new GraphQLInputObjectType({
    name: 'postInput',
    fields: () => ({
        hash: {type: GraphQLString},
        path: {type: GraphQLString},
        user_id: {type: GraphQLString},
        guild_id: {type: GraphQLString},
        created: {type: GraphQLString}
    })
})
const userInput = new GraphQLInputObjectType({
    name: 'userInput',
    fields: () => ({
        user_id: {type: GraphQLString},
        guild_id: {type: GraphQLString},
        created: {type: GraphQLString}
    })
})
const PostType = new GraphQLObjectType({
    name: 'PostType',
    fields: () => ({
        id: {type: GraphQLString},
        hash: {type: GraphQLString},
        path: {type: GraphQLString},
        user_id: {type: GraphQLString},
        guild_id: {type: GraphQLString},
        created: {type: GraphQLString}
    })
})

const UserType = new GraphQLObjectType({
    name: 'UserType',
    fields: () => ({
        id: {type: GraphQLString},
        user_id: {type: GraphQLString},
        guild_id:{type: GraphQLString},
        created: {type: GraphQLString}
    })
})
const mutations = new GraphQLObjectType({
    name: 'rootMutationType',
    fields: {
        createPost: {
            type: graphql.GraphQLBoolean,
            args: {
                input: {type: postInput}
            },
            async resolve(parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'discord_bot'
                })
                conn.connect()
                let returnarr = false
                returnarr = await addPost(args.input)
                conn.end()
                return returnarr
            }
        },
        createUser: {
            type: graphql.GraphQLBoolean,
            args: {
                input: {type: userInput}
            },
            async resolve(parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'discord_bot'
                })
                conn.connect()
                let returnarr = false
                returnarr = await addUser(args.input)
                conn.end()
                return returnarr
            }
        }
    }
})
const schema = new GraphQLObjectType({
    name: 'rootQueryType',
    fields: {
        getPosts: {
            type: GraphQLList(PostType),
            args: {
                num: {type: GraphQLInt}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'discord_bot'
                })
                conn.connect()
                let returnarr = []
                returnarr = await getPosts(args.num)
                conn.end()
                return returnarr
                
            },     
        },
        getPost: {
            type: PostType,
            args: {
                id: {type: GraphQLInt}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'discord_bot'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getPost(args.id)
                conn.end()
                return returnarr
                
            },     
        },
        getUser: {
            type: UserType,
            args: {
                id: {type: GraphQLInt}
            },
            async resolve(parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'discord_bot'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getUser(args.id)
                conn.end()
                return returnarr
            }
        },
        getPostByHash: {
            type: PostType,
            args: {
                hash: {type: GraphQLString}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'discord_bot'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getPostByHash(args.hash)
                conn.end()
                return returnarr
                
            },     
        },
        getKing: {
            type: UserType,
            args: {
                guild_id: {type: GraphQLString}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'discord_bot'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getKing(args.guild_id)
                conn.end()
                return returnarr
                
            },     
        },
    }
})
module.exports = new GraphQLSchema({
    query: schema,
    mutation: mutations
});
let getPosts =  function(num) {
    return new Promise((resolve, reject) => {    
        conn.query(`SELECT * from post limit '${num}'`, (err, rows) => {
            if (err) reject(err)
             resolve(rows)
        })
    }) 
}
let getPost =  function(id) {
    return new Promise((resolve, reject) => {    
        conn.query(`SELECT * from post where id='${id}'`, (err, rows) => {
            if (err) reject(err)
             resolve(rows[0])
        })
    }) 
}
let getPostByHash =  function(hash) {
    return new Promise((resolve, reject) => {    
        conn.query(`SELECT * from post where hash='${hash}'`, (err, rows) => {
            if (err || rows === undefined) reject(err)
            else resolve(rows[0])
        })
    }) 
}
let getUser =  function(id) {
    return new Promise((resolve, reject) => {    
        conn.query(`SELECT * from user where id='${id}'`, (err, rows) => {
            if (err) reject(err)
            resolve(rows[0])
        })
    }) 
}
let addUser = function(post) {
    return new Promise((resolve, reject) => {
        conn.query(`INSERT INTO user(user_id, guild_id, created) 
        VALUES ('${post.user_id}', '${post.guild_id}', '${post.created}')`, (err, rows) => {
            if (err) reject(err)
            resolve(true)
        })
    })
}
let addPost = function(post) {
    return new Promise((resolve, reject) => {
        conn.query(`INSERT INTO post(hash, path, user_id, guild_id, created) 
        VALUES ('${post.hash}', '${post.path}', '${post.user_id}','${post.guild_id}', '${post.created}')`, (err, rows) => {
            if (err) reject(err)
            resolve(true)
        })
    })
}
let getKing = function(guild_id) {
    return new Promise((resolve, reject) => {
        conn.query(`select user.* from user INNER JOIN post on user.user_id = post.user_id where post.guild_id='${guild_id}' GROUP BY user_id ORDER BY COUNT(post.id) DESC limit 1`, (err, rows) => {
            console.log(rows)
            if (err) reject(err)
            resolve(rows[0])
        })
    })
}
