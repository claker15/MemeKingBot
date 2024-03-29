import asyncio
import time
import disnake
from disnake.ext import commands
from disnake import FFmpegPCMAudio
import logging
from utils.query import *
from utils.points import *
import yt_dlp

logger = logging.getLogger("soundboard")
file_prefix_linux = "/home/code/MemeKingBot/bot/sounds/"
file_prefix_windows = "F:/sounds/"
FFMPEG_OPTIONS = {'options': '-vn'}


def get_sound_as_options_array(guild_id):
    sounds = all_sounds(guild_id)
    options = []
    for i in range(len(sounds)):
        options.append(disnake.SelectOption(label=sounds[i][0], value=sounds[i][0]))
    return options


async def play_sound(inter: disnake.ApplicationCommandInteraction, path):
    voice_channel = inter.author.voice.channel
    logger.info("Playing track at path: {}".format(path))
    voice_client = await voice_channel.connect()

    def my_after(error):
        coro = voice_client.disconnect()
        fut = asyncio.run_coroutine_threadsafe(coro, voice_client.loop)
        try:
            fut.result()
        except:
            pass

    voice_client.play(FFmpegPCMAudio(path, **FFMPEG_OPTIONS), after=my_after)


class Sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Play a sound using points")
    async def sounds(self, inter: disnake.CommandInteraction):
        logger.info("starting sound playing command")
        if inter.author.voice is None:
            await inter.response.send_message("Must be connected to a voice channel")
            return

        if user_points(inter.guild.id, inter.author.id) < 5:
            await inter.response.send_message("Not enough points. Need 5.")
            return

        view = DropdownView(get_sound_as_options_array(inter.guild.id), 'play')
        view.message = await inter.send(view=view)

    def sound_play(self, inter: disnake.ApplicationCommandInteraction, file_path):
        logger.info("got sound choice from user: {}".format(file_path))
        # points.sound_redemption(inter.id, inter.author.id, inter.guild.id)
        path = file_prefix_linux + str(inter.guild.id) + "/" + file_path + '.mp3'
        path = path.replace('\"', '\'')
        print(path)
        logger.info("playing sound from path: {}".format(path))
        inter.bot.loop.create_task(play_sound(inter, path))

    async def del_sound(self, inter: disnake.ApplicationCommandInteraction, sound):
        logger.info("removing sound from list")
        logger.info("inter id = {}".format(inter.id))
        # points.sound_add(inter.id, inter.author.id, inter.guild.id)
        delete_sound(sound, inter.guild.id)
        await inter.response.send_message("Sound removed successfully")

    @commands.slash_command(description="Add a new sound. 10 second time limit.")
    async def add_sound(self, inter: disnake.CommandInteraction, sound_url: str):
        logger.info("Starting addsound command")
        if sound_url == "":
            await inter.response.send_message("Need a video url")
            return
        if sound_count(inter.guild.id) >= 10:
            await inter.response.send_message("Sound limit for server reached")
            return
        if user_points(inter.guild.id, inter.author.id) < 10:
            await inter.response.send_message("Not enough points. Need 10.")
            return
        logger.info("checks passed. Getting video metadata")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': './sounds/{}/%(title)s.%(ext)s'.format(inter.guild.id),
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {'key': 'FFmpegMetadata'},
            ],
        }
        ydl_info = yt_dlp.YoutubeDL(ydl_opts)
        with ydl_info:
            metadata = ydl_info.extract_info(sound_url, download=False)
        if 'entries' in metadata:
            metadata = metadata['entries'][0]
        logger.info("Got video metadata: {}".format(metadata))
        if get_sound_by_path('./sounds/{}/{}.mp3'.format(inter.guild.id, metadata['title']), inter.guild.id):
            await inter.response.send_message("Video already exists")
            return
        if metadata['duration'] > 10:
            await inter.response.send_message("Video too long")
            return
        await inter.response.defer()
        await inter.channel.send("Starting sound download")
        logger.info("all checks passed. Downloading video and converting")
        with ydl_info:
            data = ydl_info.extract_info(sound_url, download=True)
        if 'entries' in data:
            data = data['entries'][0]
        logger.info("Adding sound with information: {}".format(data))
        add_sound(data['title'], './sounds/{}/{}.mp3'.format(inter.guild.id, data['title']), inter.guild.id)
        # points.sound_add(inter.id, inter.author.id, inter.guild.id)
        await inter.edit_original_response("Sound added successfully")

    @commands.slash_command(description="Remove a sound from the list. Costs 10 points.")
    async def delete_sound(self, inter: disnake.CommandInteraction):
        logger.info("starting delsound command")
        logger.info("inter is: {}".format(inter))
        if user_points(inter.guild.id, inter.author.id) < 10:
            await inter.response.send_message("Not enough points. Need 10.")
            return
        logger.info("checks passed. Listing sounds to user")
        view = DropdownView(get_sound_as_options_array(inter.guild.id), 'del')
        await inter.response.send_message(view=view)
        await inter.response.defer()


class DropdownView(disnake.ui.View):
    message: disnake.Message
    def __init__(self, options, operation):
        super().__init__(timeout=10)
        self.selection = ""
        self.add_item(Dropdown(options, operation))

    async def on_timeout(self):
        self.clear_items()
        await self.message.edit(view=self)


class Dropdown(disnake.ui.StringSelect):
    def __init__(self, options, operation):
        super().__init__(
            placeholder="Choose a sound",
            min_values=1,
            max_values=1,
            options=options
        )
        self.operation = operation

    async def callback(self, inter: disnake.CommandInteraction):
        logger.info("got into dropdown callback")
        if self.operation == 'play':
            await inter.response.send_message("Playing sound {}".format(self.values[0]))
            Sounds.sound_play(self, inter, self.values[0])
        if self.operation == 'del':
            await inter.response.send_message("Removing sound chosen")
            await Sounds.del_sound(self, inter, self.values[0])
        self.disabled = True
        await self.view.message.edit(view=self.view)


def setup(bot):
    return bot.add_cog(Sounds(bot))
