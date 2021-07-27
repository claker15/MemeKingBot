import logging

from numpy.lib.function_base import extract
import discord
import os
import logging
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import re
import requests
import datetime
from io import BytesIO
import imagehash
from PIL import Image
from urlextract import URLExtract
from hashlib import sha256
import query as query
import points as points

load_dotenv()
url = os.getenv("BOT_API_URL")
file_save_path = os.getenv("FILE_SAVE_PATH")
logger = logging.getLogger("message")

async def parse_message(message):
    urls = extract_urls(message.content)
    if len(urls) > 0:
        logger.debug("urls found in message")
        await process_urls(message)
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
    await channel.send(content="@{0}".format(author.nick), file=discord.File(fp="/home/memes/Relax.png"))

async def send_cringe_message(author, channel):
    logger.debug("post exists. sending cringe message")
    await channel.send("@{0} Cringe. Old meme,   :b:ruh https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png".format(author.nick))

def save_attachments(image, filename):
    logger.debug("saving new image with filename: {0}".format(filename))
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
        new_hash = str(imagehash.whash(Image.open(BytesIO(res.content))))
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
            points.relax_points(message.guild.id, message.author.id)
            await send_relax_message(message.author, message.channel)
            return
        if post != None:
            points.cringe_points(post["user_id"], message.guild.id, message.author.id)
            await send_cringe_message(message.author, message.channel)
            return
        points.reg_points(message.author.id, message.guild.id)

def get_urls(string):
    extractor = URLExtract()
    urls = extractor.find_urls(string)
    logger.debug("found urls {0}".format(urls))
    return urls

def strip_url(url):

    query = urlparse(url)
    
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    elif 'i.redd.it' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError

async def process_urls(message):
    logger.debug("starting profcessing urls in message {0}".format(message.content))
    urls = get_urls(message.content)
    for url in urls:
        logger.debug("start parsing url: {0}".format(url))
        video_id = strip_url(url)
        res = query.get_post_by_hash(video_id, message.guild.id)
        cooldown = cool_down(message.author.id, message.guild.id)
        #save image if not there
        if res == None:
            obj = create_post_object(video_id, url, message.author.id, message.guild.id)
            query.create_post(obj)
        #send cooldown message if 
        if cooldown:
            points.relax_points(message.guild.id, message.author.id)
            await send_relax_message(message.author, message.channel)
            return
        if res != None:
            points.cringe_points(res["user_id"], message.guild.id, message.author.id)
            await send_cringe_message(message.author, message.channel)
            return
        points.reg_points(message.author.id, message.guild.id)

