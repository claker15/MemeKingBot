
const graphql = require('graphql')
var { graphqlHTTP, GraphQLObjectType, GraphQLString, GraphQLSchema, GraphQLList, GraphQLInt, GraphQLD, GraphQLInputObjectType} = graphql;
const mysql = require('mysql');



let conn = mysql.createConnection({
    host: 'localhost',
    user: 'api',
    password: 'apipassword',
    database: 'MEMEKING'
})
const postInput = new GraphQLInputObjectType({
    name: 'postInput',
    fields: () => ({
        hash: {type: GraphQLString},
        path: {type: GraphQLString},
        user_id: {type: GraphQLString},
        guild_id: {type: GraphQLString},
        message_id: {type: GraphQLString},
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
const pointInput = new GraphQLInputObjectType({
    name: 'pointInput',
    fields: () => ({
        user_id: {type: GraphQLString},
        guild_id: {type: GraphQLString},
        user_id_from: {type: GraphQLString},
        value: {type: GraphQLInt},
        type: {type: GraphQLString},
        message_id: {type: GraphQLString}
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
        message_id: {type: GraphQLString},
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
const pointType = new GraphQLObjectType({
    name: 'PointType',
    fields: () => ({
        id: {type: GraphQLString},
        user_id: {type: GraphQLString},
        guild_id:{type: GraphQLString},
        user_id_from: {type: GraphQLString},
        value: {type: GraphQLInt},
        type: {type: GraphQLString},
        message_id: {type: GraphQLString},
        date: {type: GraphQLString}
    })
})
const RankType = new GraphQLObjectType({
    name: 'RankType',
    fields: () => ({
        user_id: {type: GraphQLString},
        count: {type: GraphQLInt}
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
                    database: 'MEMEKING'
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
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = false
                returnarr = await addUser(args.input)
                conn.end()
                return returnarr
            }
        },
        changeKingCount: {
            type: graphql.GraphQLBoolean,
            args: {
                input: {type: userInput},
            },
            async resolve(parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = false
                returnarr = await changeKingCount(args.input)
                conn.end()
                return returnarr
            }
        },
        addPoints: {
            type: graphql.GraphQLBoolean,
            args: {
                input: {type: pointInput}
            },
            async resolve(parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = false
                returnarr = await addPoints(args.input)
                conn.end()
                return returnarr
            }
        },
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
                    database: 'MEMEKING'
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
                    database: 'MEMEKING'
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
                    database: 'MEMEKING'
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
                hash: {type: GraphQLString},
                guild_id: {type: GraphQLString}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getPostByHash(args.hash, args.guild_id)
                conn.end()
                return returnarr
                
            },
        },
        getPostByPath: {
            type: PostType,
            args: {
                path: {type: GraphQLString},
                guild_id: {type: GraphQLString}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getPostByPath(args.path, args.guild_id)
                conn.end()
                return returnarr 
            },     
        },
        getPreviousPost: {
            type: PostType,
            args: {
                user_id: {type: GraphQLString},
                guild_id: {type: GraphQLString}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getPreviousPost(args.user_id, args.guild_id)
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
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getKing(args.guild_id)
                conn.end()
                return returnarr
                
            },     
        },
        getRanking : {
            type: GraphQLList(RankType),
            args: {
                guild_id :{type: GraphQLString}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getRanking(args.guild_id)
                conn.end()
                return returnarr
            }
        },
        getCrowns : {
            type: GraphQLList(RankType),
            args: {
                guild_id :{type: GraphQLString}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getCrowns(args.guild_id)
                conn.end()
                return returnarr
            }
        },
        getRandomUserId: {
            type: PostType,
            args: {
                guild_id: {type: GraphQLString}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: 'localhost',
                    user: 'api',
                    password: 'apipassword',
                    database: 'MEMEKING'
                })
                conn.connect()
                let returnarr = {}
                returnarr = await getRandomUserId(args.guild_id)
                conn.end()
                return returnarr
            }
        }
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
let getPostByHash =  function(hash, guild_id) {
    return new Promise((resolve, reject) => {    
        conn.query(`SELECT * from post where hash='${hash}' and guild_id='${guild_id}'`, (err, rows) => {
            if (err || rows === undefined) reject(err)
            resolve(rows[0])
        })
    }) 
}
let getPostByPath =  function(path, guild_id) {
    return new Promise((resolve, reject) => {    
        conn.query(`SELECT * from post where path='${path}' and guild_id='${guild_id}'`, (err, rows) => {
            if (err || rows === undefined) reject(err)
            resolve(rows[0])
        })
    }) 
}
let getPreviousPost =  function(user_id, guild_id) {
    return new Promise((resolve, reject) => {    
        conn.query(`select * from post where user_id='${user_id}' AND guild_id='${guild_id}' ORDER BY created DESC LIMIT 1`, (err, rows) => {
            if (err || rows === undefined) reject(err)
            resolve(rows[0])
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
        conn.query(`INSERT INTO user(user_id, guild_id, created, crowns) 
        VALUES ('${post.user_id}', '${post.guild_id}', NOW(), 0)`, (err, rows) => {
            if (err) reject(err)
            resolve(true)
        })
    })
}
let addPost = function(post) {
    console.log(post)
    return new Promise((resolve, reject) => {
        conn.query(`INSERT INTO post(hash, path, user_id, guild_id, message_id, created) 
        VALUES ('${post.hash}', '${post.path}', '${post.user_id}','${post.guild_id}', '${post.message_id}', NOW())`, (err, rows) => {
            console.log(rows)
            if (err) reject(err)
            resolve(true)
        })
    })
}
let getKing = function(guild_id) {
    return new Promise((resolve, reject) => {
        conn.query(`select user_id, SUM(value) as count from points where guild_id='${guild_id}' 
                    AND  YEARWEEK(date) = YEARWEEK(NOW() - INTERVAL 1 WEEK)
                    GROUP BY user_id ORDER BY SUM(value) DESC LIMIT 1 ;`, (err, rows) => {
            if (err) reject(err)
            resolve(rows[0])
        })
    })
}
let getRanking = function(guild_id) {
    return new Promise((resolve, reject) => {
        conn.query(`SELECT user_id, SUM(value) as count FROM points WHERE guild_id = '${guild_id}' AND YEARWEEK(date) = YEARWEEK(NOW())
        GROUP BY user_id ORDER BY SUM(value) DESC LIMIT 5 ;`, (err, rows) => {
            if (err) reject(err)
            resolve(rows)
        })
    })
}
let getCrowns = function(guild_id) {
    return new Promise((resolve, reject) => {
        conn.query(`select user_id, crowns as count from user where guild_id='${guild_id}'  
                    GROUP BY user_id ORDER BY count DESC limit 5;`, (err, rows) => {
            if (err) reject(err)
            resolve(rows)
        })
    })
}
let changeKingCount = function(input) {
    return new Promise((resolve, reject) => {
        conn.query(`INSERT INTO user(user_id, guild_id, created, crowns) VALUES (${input.user_id},${input.guild_id},NOW(),1)
        ON DUPLICATE KEY UPDATE crowns = crowns+1;`, (err, rows) => {
            if (err) reject(err)
            resolve(true)

        })
    })
}
let addPoints = function(point) {
    console.log(point)
    return new Promise((resolve, reject) => {
        conn.query(`INSERT INTO points(user_id, guild_id, user_id_from, value, type, message_id) 
        VALUES ('${point.user_id}', '${point.guild_id}', '${point.user_id_from}', ${point.value},'${point.type}', '${point.message_id}')`, (err, rows) => {
            if (err) reject(err)
            resolve(true)
        })
    })
}
let getRandomUserId =  function(guild_id) {
    return new Promise((resolve, reject) => {    
        conn.query(`select * from post where guild_id = '${guild_id}' ORDER BY RAND() LIMIT 1;`, (err, rows) => {
            if (err) reject(err)
            resolve(rows[0])
        })
    }) 
}
