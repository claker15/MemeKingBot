var express =  require('express');
var {graphqlHTTP} = require('express-graphql');
var bodyParser = require('body-parser');
var mysql = require('mysql');
let schema = require('./schema.js');
var cors = require('cors');

var app = express();
let whitelist = ['http://localhost:4000', 'http://192.168.1.86:4000', 'https://76.245.71.164:4000', 'http://8.9.113.62:4000'];
/*app.use(cors({
    origin: function(origin, callback){
      // allow requests with no origin 
      if(!origin) return callback(null, true);
      if(whitelist.indexOf(origin) === -1){
        var message = `The CORS policy for this origin doesn't
                  allow access from the particular origin.`;
        return callback(new Error(message), false);
      }
      return callback(null, true);
    }
  }));*/
app.use(bodyParser.json());

app.use('/graphql', graphqlHTTP({
    schema: schema,
    graphiql: true
}));
app.listen(4000, () => console.log("Server listing on port 4000"));
