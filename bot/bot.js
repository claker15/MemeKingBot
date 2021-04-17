const discord = require('discord.js');
const fs = require('fs')
const schedule = require('node-schedule');
const config = require('./config.json');

let tally = []

const client = new discord.Client();
client.commands = new discord.Collection();

const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'))
const eventFiles = fs.readdirSync('./events').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	client.commands.set(command.name, command);
}
for (const file of eventFiles) {
	const event = require(`./events/${file}`);
	if (event.once) {
		client.once(event.name, (...args) => event.execute(...args, client));
	} else {
		client.on(event.name, (...args) => event.execute(...args, client, tally));
	}
}

const coronation = schedule.scheduleJob("0 * * * * *", () => {
    client.emit("crown")
})

botSecretToken = config.token

client.login(botSecretToken);
