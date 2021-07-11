import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("BOT_API_URL")
crown_guilds = os.getenv("CROWN_GUILDS").split(',')
crown_channels = os.getenv("CROWN_CHANNELS").split(',')

kingQuery = """query getKing($guild_id: String) {
                                getKing(guild_id: $guild_id){
                                    user_id
                                }
                    }"""
changeCrownQuery = """mutation changeKingCount($input: userInput) {
                            changeKingCount(input: $input)
                        }"""

async def crown(ctx):
    for index, guild_id in enumerate(crown_guilds):
        print("finding user_id for king on server {0}".format(guild_id))
        guild = await ctx.fetch_guild(guild_id)
        res = requests.post(url, json={"query": kingQuery, "variables": {"guild_id": str(guild_id)}})
        print(res)
        user = res.json()
        print(user["data"]["getKing"])
        user_id = res.json()["data"]["getKing"]["user_id"]
        print(user_id)
        member = await guild.fetch_member(user_id)
        obj = {
            "user_id": user_id,
            "guild_id": guild_id
        }
        res = requests.post(url, json={"query": changeCrownQuery, "variables": {"input": obj}})
        print(res.text)
        print(crown_channels[index])
        channel = discord.utils.get(await guild.fetch_channels(), name=crown_channels[index])
        print(channel)
        await channel.send("👑{0} is Meme King of the Week 👑".format(member.nick))
        print("succesfully crowned {0} for server {1}".format(member.nick, guild_id))

