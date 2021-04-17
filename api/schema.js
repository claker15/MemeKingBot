var { graphqlHTTP } = require('express-graphql');
var { buildSchema } = require('graphql');

const schema = buildSchema(`
    type Query {
        hello: String
    }`);

module.exports = schema;