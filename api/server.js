import express from 'express'
import graphqlHTTP from 'express-graphql'
import bodyParser from 'body-parser'
import mysql from 'mysql'
let schema = require('./schema.js')


let conn = mysql.createConnection({
    host: 'localhost',
    user: 'api',
    password: 'apipassword',
    database: 'discord_bot'
})

/*conn.connect()

conn.query('SELECT * from post', (err, rows, fields) => {
    if (err) throw err
    console.log(rows)
})*/

var root = { hello: () => 'hello world'};

var app = express()
app.use(bodyParser.json())

app.use('/graphql', graphqlHTTP(req => ({
    schema: schema,
    rootValue: root,
    qraphiql: true,
})))
app.listen(4000, () => console.log("Server listing on port 4000"))