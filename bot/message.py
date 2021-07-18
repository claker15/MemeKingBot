import logging
import discord
import os
import logging
from dotenv import load_dotenv
from urllib.parse import urlparse
import re
import requests
import datetime
from urlextract import URLExtract
from hashlib import sha256
import query as query
import points as points

coolDownQuery = """query getPreviousPost($user_id: String, $guild_id: String){
                    getPreviousPost(user_id: $user_id, guild_id: $guild_id) {
                        created
                    }
                }"""

postByHashQuery = """query getPostByHash($hash: String, $guild_id: String){
                    getPostByHash(hash: $hash, guild_id: $guild_id) {
                        hash
                        path
                    }
                }"""
createPost = """mutation createPost($input: postInput) {
                    createPost(input: $input)
        }"""

load_dotenv()
url = os.getenv("BOT_API_URL")
file_save_path = os.getenv("FILE_SAVE_PATH")
logger = logging.getLogger("message")

async def parse_message(message):
    urls = extract_urls(message.content)
    if len(urls) > 0:
        logger.debug("urls found in message")
        process_urls(urls)
        #process youtube or other urls
        return
    if len(message.attachments) > 0:
        logger.debug("attachments found in message")
        await process_attachments(message)

def extract_urls(content):
    extractor = URLExtract()
    urls = extractor.find_urls(content)
    return urls

def create_post_object(hash, path, user_id, guild_id):
    obj = {
        "hash": hash,
        "path": path,
        "user_id": str(user_id),
        "guild_id": str(guild_id)
    }
    return obj

async def send_relax_message(author, channel):
    logger.debug("{0} has not waited for cooldown period".format(author.id))
    file = discord.File(fp="/home/memes/Relax.png")
    await channel.send(content="@{0}".format(author.nick), file=file)

async def send_cringe_message(author, channel):
    logger.debug("post exists. sending cringe message")
    await channel.send("@{0} Cringe. Old meme,   :b:ruh https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png".format(author.nick))

def save_attachments(image, filename):
    logger.debug("saving new image with filename: {}".format(filename))
    with open(file_save_path + filename, 'wb') as outfile:
                for chunk in image:
                    outfile.write(chunk)

def cool_down(author_id, guild_id):
    logging.debug("starting cooldown check for user: {0} in guild: {1}".format(author_id, guild_id))
    prev_time = datetime.datetime.fromtimestamp(query.get_user_cooldown_date(author_id, guild_id)/1000.0)
    now = datetime.datetime.now()
    diff_time = (now - prev_time).seconds / 60.0
    logger.debug("{0} minutes since last post from user: {1}".format(diff_time, author_id))
    if diff_time < 5.0:
        return True
    else:
        return False

async def process_attachments(message):
    logger.debug("starting attachment processing for message {0}".format(message.id))
    for attach in message.attachments:
        logger.debug("processing message attachment: {0}".format(attach.url))
        res = requests.get(attach.url)
        new_hash = sha256(res.content).hexdigest()
        image = res
        logger.debug("image hashed to: {0}".format(new_hash)) 
        post = query.get_post_by_hash(new_hash, message.guild.id)
        cooldown = cool_down(message.author.id, message.guild.id)
        #save image if not there
        if post == None:
            save_attachments(image, attach.filename)
            obj = create_post_object(new_hash, file_save_path + attach.filename, message.author.id, message.guild.id)
            query.create_post(obj)
        #send cooldown message if 
        if cooldown:
            points.relax_points(message.guild.id)
            send_relax_message(message.author, message.channel)
            return
        if post != None:
            points.cringe_points(post["user_id"], message.guild.id)
            send_cringe_message(message.author, message.channel)
            return

def get_urls(string):
    url = re.findall("(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", string)
    return [x[0] for x in url]

def strip_youtube_url(url):

        if url.startswith('http://'):
            url = url[7:]
        elif url.startswith('https://'):
            url = url[8:]

        if url.startswith('www.'):
            url = url[4:]

        if url.startswith('youtu.be/'):
            return url[9:]
        elif url.startswith('youtube.com/v/'):
            return url[14:]

        return url

async def process_urls(message):
    logger.debug("starting profcessing urls in message {0}".format(message.id))
    urls = get_urls(message.content)
    for url in urls:
        logger.debug("start parsing url: {0}".format(url))
        video_id = strip_youtube_url(url)
        res = query.get_post_by_hash(video_id, message.guild.id)
        cooldown = cool_down(message.author.id, message.guild.id)
        #save image if not there
        if res == None:
            obj = create_post_object(video_id, url, message.author.id, message.guild.id)
            query.create_post(obj)
        #send cooldown message if 
        if cooldown:
            points.relax_points(message.guild.id)
            send_relax_message(message.author, message.channel)
            return
        if res != None:
            points.cringe_points(res["user_id"], message.guild.id)
            send_cringe_message(message.author, message.channel)
            return


