import asyncio
import discord
from discord.ext import commands
import requests
import logging
import random
import points as points
import html
import json

logger = logging.getLogger("trivia")


class Question:
    def __init__(self, category, question, answers, correct_answer, diff):
        self.category = category
        self.question = question
        self.answers = answers
        for i in range(len(answers)):
            if answers[i] == correct_answer:
                self.correct_index = i
        self.difficulty = diff

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia_urls = []
        with open("trivia_urls.json") as file:
            self.trivia_urls = json.load(file)['urls']
        self.letters = ['A', 'B', 'C', 'D']
        self.emojis = ['🇦', '🇧', '🇨', '🇩']
        self.emoji_to_index = {'🇦': 0,
                               '🇧': 1,
                               '🇨': 2,
                               '🇩': 3}
        self.difficulty_scale = {'easy': 1, "medium": 2, "hard": 3}

    def get_question(self):
        logger.debug("getting trivia answer from api")
        trivia_url = random.choice(self.trivia_urls)
        if trivia_url['category'] is None:
            trivia_url['category'] = ''
        if trivia_url['difficulty'] is None:
            trivia_url['difficulty'] = ''
        print(trivia_url['url'])
        res = requests.get(trivia_url['url'])
        logger.debug('Got request from trivia api: {}'.format(res))
        print(res.json())
        if trivia_url['results_response'] != "":
            results = res.json()[trivia_url['results_response']][0]
        else:
            results = res.json()[0]
        answers = []
        answers.append(results[trivia_url['correct_string']])
        answers = answers + results[trivia_url['incorrect_string']]
        random.shuffle(answers)
        trivia_obj = Question(results[trivia_url['category']], results[trivia_url['question']], answers, results[trivia_url['correct_string']], results[trivia_url['difficulty']])
        return trivia_obj

    def create_message(self, question):
        embed = discord.Embed()
        embed.title = "Trivia Question"
        embed.add_field(name="Difficulty", value=html.unescape(question.difficulty), inline=False)
        embed.add_field(name='Category', value=html.unescape(question.category), inline=False)
        embed.add_field(name='Question', value=html.unescape(question.question), inline=False)
        for i in range(len(question.answers)):
            embed.add_field(name=self.letters[i], value=html.unescape(question.answers[i]), inline=True)
        return embed

    @commands.command()
    async def trivia(self, ctx: commands.Context):
        logger.debug("starting trivia command")
        question = self.get_question()
        embed = self.create_message(question)
        message = await ctx.reply(embed=embed)
        for i in range(len(self.emojis)):
            await message.add_reaction(self.emojis[i])

        def check(reaction, user):
            return user == ctx.message.author and reaction.emoji in self.emojis and reaction.count > 1

        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=check)
            if self.emoji_to_index.get(reaction.emoji) is not None and self.emoji_to_index[
                reaction.emoji] == question.correct_index and reaction.count > 1:
                logger.debug("got correct user and correct answer, adding points to user {}".format(user))
                points.trivia_correct_answer(ctx.message.id, ctx.message.author.id, ctx.guild.id,
                                             self.difficulty_scale[question.difficulty])
                await ctx.reply("Correct Answer")
            else:
                await ctx.reply("Wrong Answer. It was {}".format(html.unescape(question.answers[question.correct_index])))

        except asyncio.TimeoutError:
            await ctx.reply("Took too long to answer")


def setup(bot):
    return bot.add_cog(Trivia(bot))
