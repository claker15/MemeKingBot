# MemeKingBot

### Find out who is the meme king of the week with MemeKingBot

## Usage:
Not that I am expecting anyone to use this, but just run bot.js and the bot will start. In the same folder level, a config.js file must exists with the following fields:
- prefix: This is the prefix to use to use a command.
- token: This is the secret token from the discord api and is needed for bot to function.
- servers: List of servers/guild ids that the bot is a member of/tracks. This does not add the bot to the server, so that must be done first.
- channel_name: List of text channel names that the bot should annouce the king to. The text channels for servers in the servers list should match indecies. For example, as list of servers like ['123456', '789'] and a channel_name list of ['general', 'main'] means that the king of server 123456 is announced in the text channel on that server called general.
- file_path: Path that images will be saved to.
- api_server_url: Url that is used to make request to api layer of app.