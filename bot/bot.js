const discord = require('discord.js');
const fs = require('fs')
const schedule = require('node-schedule');
const config = require('./config.json');

const client = new discord.Client();
client.commands = new discord.Collection();

const commandFiles = fs.readdirSync(config.run_path + '/commands').filter(file => file.endsWith('.js'))
const eventFiles = fs.readdirSync(config.run_path + '/events').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	client.commands.set(command.name, command);
}
for (const file of eventFiles) {
	const event = require(`./events/${file}`);
	if (event.once) {
		client.once(event.name, (...args) => event.execute(...args, client));
	} else {
		client.on(event.name, (...args) => event.execute(...args, client));
	}
}

const rule = new schedule.RecurrenceRule();
rule.dayOfWeek = 0;
rule.hour = 0;
rule.minute = 0;
rule.second = 0;
rule.tz = "America/Indiana/Indianapolis";

const coronation = schedule.scheduleJob(rule, () => {
    client.emit("crown")
})

client.login(config.token);
