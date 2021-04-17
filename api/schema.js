const { json } = require('body-parser');
const graphql = require('graphql')
var { graphqlHTTP, GraphQLObjectType, GraphQLString, GraphQLSchema, GraphQLList, GraphQLInt, GraphQLD} = graphql;
var { buildSchema } = require('graphql');
const mysql = require('mysql');

let conn = mysql.createConnection({
    host: '192.168.1.86',
    user: 'api',
    password: 'apipassword',
    database: 'discord_bot'
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

const schema = new GraphQLObjectType({
    name: 'rootQueryType',
    fields: {
        posts: {
            type: GraphQLList(PostType),
            args: {
                num: {type: GraphQLInt}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: '192.168.1.86',
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
        post: {
            type: GraphQLList(PostType),
            args: {
                id: {type: GraphQLInt}
            },
            async resolve (parent, args) {
                let conn = mysql.createConnection({
                    host: '192.168.1.86',
                    user: 'api',
                    password: 'apipassword',
                    database: 'discord_bot'
                })
                conn.connect()
                let returnarr = []
                returnarr = await getPost(args.id)
                conn.end()
                return returnarr
                
            },     
        },
    }
})
module.exports = new GraphQLSchema({
    query: schema
});
let getPosts =  function(num) {
    return new Promise((resolve, reject) => {    
        conn.query(`SELECT * from post limit ${num}`, (err, rows) => {
            if (err) reject(err)
             resolve(rows)
        })
    }) 
}
let getPost =  function(id) {
    return new Promise((resolve, reject) => {    
        conn.query(`SELECT * from post where id=${id}`, (err, rows) => {
            if (err) reject(err)
             resolve(rows)
        })
    }) 
}