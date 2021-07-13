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
        if cool_down(message.author.id, message.guild.id):
            logger.debug("{0} has not waited for cooldown period".format(message.author.id))
            file = discord.File(fp="/home/memes/Relax.png")
            await message.channel.send(content="@{0}".format(message.author.nick), file=file)
            return
        process_urls(urls)
        #process youtube or other urls
        return
    if len(message.attachments) > 0:
        logger.debug("attachments found in message")
        if cool_down(message.author.id, message.guild.id):
            logger.debug("{0} has not waited for cooldown period".format(message.author.id))
            file = discord.File(fp="/home/memes/Relax.png")
            await message.channel.send(content="@{0}".format(message.author.nick), file=file)
            return
        await process_attachments(message)

def extract_urls(content):
    extractor = URLExtract()
    urls = extractor.find_urls(content)
    return urls
    
def cool_down(author_id, guild_id):
    logging.debug("starting cooldown check for user: {0} in guild: {1}".format(author_id, guild_id))
    author_id_str = str(author_id)
    guild_id_str = str(guild_id)
    logger.debug("Getting cooldown time for user: {0} in guild {1}".format(author_id, guild_id))
    res = requests.post(url, json={"query": coolDownQuery, "variables": {"user_id": author_id_str, "guild_id": guild_id_str}})
    post = res.json()
    logger.debug("received post from database".format(post["data"]["getPreviousPost"]))
    prev_time = datetime.datetime.fromtimestamp(int(post["data"]["getPreviousPost"]["created"])/1000.0)
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
        res = requests.post(url, json={"query": postByHashQuery, "variables": {"hash": new_hash, "guild_id": str(message.guild.id)}})
        post = res.json()["data"]["getPostByHash"]
        logger.debug("post returned from getPostByHash query: {0}".format(post))
        if post != None:
            logger.debug("post exists with hash: {0}".format(post))
            await message.channel.send("@{0} Cringe. Old meme,   :b:ruh https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png".format(message.author.nick))
            return
        else:
            with open(file_save_path + attach.filename, 'wb') as outfile:
                for chunk in image:
                    outfile.write(chunk)
            obj = {
                "hash": new_hash,
                "path": file_save_path + attach.filename,
                "user_id": str(message.author.id),
                "guild_id": str(message.guild.id)
            }
            logger.debug("Sending new post object to database: {0}".format(obj))
            res = requests.post(url, json={"query": createPost, "variables": {"input": obj}})
            logger.debug("received as response from createPost query: {}".format(res.content))

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
        res = requests.post(url, json={"query": postByHashQuery, "variables": {"hash": video_id, "guild_id": str(message.guild.id)}})
        logger.debug("response from getPostByHash query return json: {0}".format(res.json()))
        if res.json()["data"]["getPostByHash"] != None:
            logger.debug("post exists with hash: {0}".format(res.json()["data"]["getPostByHash"]))
            await message.channel.send("@{0} Cringe. Old meme,   :b:ruh https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png".format(message.author.nick))
        else:
            obj = {
                "hash": video_id,
                "path": url,
                "user_id": str(message.author.id),
                "guild_id": str(message.guild.id)
            }
            logger.debug("Sending object to database: {0}".format(obj))
            res = requests.post(url, json={"query": createPost, "variables": {"input": obj}})
            logger.debug("received as response from createPost query: {}".format(res.text))



