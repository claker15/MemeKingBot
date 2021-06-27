import discord
import requests
import json
from discord.ext import commands


rankQuery = """query getRanking($guild_id: String){
                        getRanking(guild_id: $guild_id) {
                            user_id,
                            count
                        }
                    }"""
crownsQuery = """query getCrowns($guild_id: String){
                        getCrowns(guild_id: $guild_id) {
                            user_id,
                            count
                        }
                    }"""
url = "http://localhost:4000/graphql"

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ranking(self, ctx: commands.Context):
        guild_id = str(ctx.guild.id)
        res = requests.post(url, json={'query': rankQuery, 'variables': {"guild_id": guild_id}})
        users = res.json()
        embed = discord.Embed(title="Current Meme King Rankings", colour=0x0099ff)
        for user in users["data"]["getRanking"]:
            member = await ctx.guild.fetch_member(user["user_id"])
            embed.add_field(name=member.nick, value=user["count"], inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def crowns(self, ctx: commands.Context):
        guild_id = str(ctx.guild.id)
        res = requests.post(url, json={'query': crownsQuery, 'variables': {"guild_id": guild_id}})
        users = res.json()
        embed = discord.Embed(title="Coronation Leaderboard 👑", colour=0x0099ff)
        for user in users["data"]["getCrowns"]:
            member = await ctx.guild.fetch_member(user["user_id"])
            embed.add_field(name=member.nick, value=user["count"], inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    return bot.add_cog(Ranking(bot))

