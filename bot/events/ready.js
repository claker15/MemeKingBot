module.exports = {
    name: 'ready',
    once: 'true',
    execute(client) {
        console.log("connected as " + client.user.tag);
    }
}