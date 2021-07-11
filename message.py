import discord
import os
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

async def parse_message(message):
    urls = extract_urls(message.content)
    if len(urls) > 0:
        print("urls exists")
        if cool_down(message.author.id, message.guild.id):
            print(message.author)
            file = discord.File(fp="/home/memes/Relax.png")
            await message.channel.send(content="@{0}".format(message.author.nick), file=file)
            return
        process_urls(urls)
        #process youtube or other urls
        return
    if len(message.attachments) > 0:
        print("attachments exist")
        if cool_down(message.author.id, message.guild.id):
            file = discord.File(fp="/home/memes/Relax.png")
            await message.channel.send(content="@{0}".format(message.author.nick), file=file)
            return
        await process_attachments(message)

def extract_urls(content):
    extractor = URLExtract()
    urls = extractor.find_urls(content)
    return urls
    
def cool_down(author_id, guild_id):
    author_id_str = str(author_id)
    guild_id_str = str(guild_id)
    res = requests.post(url, json={"query": coolDownQuery, "variables": {"user_id": author_id_str, "guild_id": guild_id_str}})
    post = res.json()
    print(post["data"]["getPreviousPost"])
    prev_time = datetime.datetime.fromtimestamp(int(post["data"]["getPreviousPost"]["created"])/1000.0)
    now = datetime.datetime.now()
    diff_time = (now - prev_time).seconds / 60.0
    print(diff_time)
    if diff_time < 5.0:
        return True
    else:
        return False

async def process_attachments(message):
    for attach in message.attachments:
        res = requests.get(attach.url)
        new_hash = sha256(res.content).hexdigest()
        image = res
        print(new_hash)
        res = requests.post(url, json={"query": postByHashQuery, "variables": {"hash": new_hash, "guild_id": str(message.guild.id)}})
        post = res.json()["data"]["getPostByHash"]
        print(post)
        if post != None:
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
            print(obj)
            res = requests.post(url, json={"query": createPost, "variables": {"input": obj}})
            print(res)
            print(res.content)
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
    urls = get_urls(message.content)
    for url in urls:
        video_id = strip_youtube_url(url)
        res = requests.post(url, json={"query": postByHashQuery, "variables": {"hash": video_id, "guild_id": str(message.guild.id)}})
        if res.json()["data"]["getPostByHash"] != None:
             await message.channel.send("@{0} Cringe. Old meme,   :b:ruh https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png".format(message.author.nick))
        else:
            obj = {
                "hash": video_id,
                "path": url,
                "user_id": str(message.author.id),
                "guild_id": str(message.guild.id)
            }
            print(obj)
            res = requests.post(url, json={"query": createPost, "variables": {"input": obj}})
            print(res)



