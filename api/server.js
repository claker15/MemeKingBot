var express =  require('express')
var {graphqlHTTP} = require('express-graphql')
var bodyParser = require('body-parser')
var mysql = require('mysql')
let schema = require('./schema.js')




/*conn.connect()

conn.query('SELECT * from post', (err, rows, fields) => {
    if (err) throw err
    console.log(rows)
})*/



var app = express()
app.use(bodyParser.json())

app.use('/graphql', graphqlHTTP({
    schema: schema,
    graphiql: true
}))
app.listen(4000, () => console.log("Server listing on port 4000"))