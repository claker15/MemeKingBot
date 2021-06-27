import discord
import requests
import datetime
from urlextract import URLExtract

coolDownQuery = """query getPreviousPost($user_id: String, $guild_id: String){
                    getPreviousPost(user_id: $user_id, guild_id: $guild_id) {
                        created
                    }
                }"""
url = "http://localhost:4000/graphql"

async def parse_message(message):
    if message.content == "":
        return
    if cool_down(message.author.id, message.guild.id):
        await message.channel.send("{0.nick} https://cdn.discordapp.com/attachments/759174594933817365/857718366491639828/Relax.png`".format(message.author))
        return
    urls = extract_urls(message)
    if len(urls) > 0:
        process_urls(urls)
        #process youtube or other urls
        return
    if len(message.attachments) > 0:
        process_attachments(message)
        return




def extract_urls(content):
    extractor = URLExtract()
    urls = extractor.find_urls(content)
    return urls
    
def cool_down(author_id, guild_id):
    res = requests.post(url, json={"query": coolDownQuery, "variables": {"user_id": author_id, "guild_id": guild_id}})
    post = res.json()
    prev_time = datetime.datetime(post["data"]["getRanking"]["created"])
    now = datetime.now()
    diff_time = (now - prev_time).seconds / 60
    if diff_time < 5:
        return True
    else:
        return False

def process_attachments(message):
    #to-do: handle attachments going to server
    return

def process_urls(message):
    #to-do: process youtube urls
    return