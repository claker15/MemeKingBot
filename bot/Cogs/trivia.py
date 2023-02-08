import asyncio
import disnake
from disnake.ext import commands
import requests
import logging
import random
import datetime
import query as query
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

    def cool_down(self, author_id, guild_id):
        logging.debug("starting cooldown check for user: {0} in guild: {1}".format(author_id, guild_id))
        last_post_time = query.trivia_cooldown(author_id, guild_id)
        if last_post_time is None:
            return False
        now = datetime.datetime.now()
        diff_time = (now - last_post_time).seconds / 60.0
        logger.debug("{0} minutes since last post from user: {1}".format(diff_time, author_id))
        if diff_time < 5.0:
            return True
        else:
            return False

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
        embed = disnake.Embed()
        embed.title = "Trivia Question"
        embed.add_field(name="Difficulty", value=html.unescape(question.difficulty), inline=False)
        embed.add_field(name='Category', value=html.unescape(question.category), inline=False)
        embed.add_field(name='Question', value=html.unescape(question.question), inline=False)
        for i in range(len(question.answers)):
            embed.add_field(name=self.letters[i], value=html.unescape(question.answers[i]), inline=True)
        return embed

    @commands.slash_command(description="Answer a trivia question for points")
    async def trivia(self, inter: disnake.CommandInteraction):
        logger.debug("starting trivia command")
        if self.cool_down(inter.author.id, inter.guild.id):
            logger.debug("trvia debug 0")
            await inter.response.reply("On cooldown")
            logger.debug("trvia debug 1")
            return
        logger.debug("trvia debug 2")
        question = self.get_question()
        logger.debug("trvia debug 3")
        embed = self.create_message(question)
        logger.debug("trvia debug 4")
        message = await inter.response.reply(embed=embed)
        logger.debug("trvia debug 5")
        for i in range(len(self.emojis)):
            await message.add_reaction(self.emojis[i])

        def check(reaction, user):
            return user == inter.author and reaction.emoji in self.emojis and reaction.count > 1

        try:
            reaction, user = await inter.bot.wait_for('reaction_add', timeout=20.0, check=check)
            if self.emoji_to_index.get(reaction.emoji) is not None and self.emoji_to_index[
                 reaction.emoji] == question.correct_index and reaction.count > 1:
                logger.debug("got correct user and correct answer, adding points to user {}".format(user))
                points.trivia_correct_answer(inter.id, inter.author.id, inter.guild.id,
                                      self.difficulty_scale[question.difficulty])
                await inter.response.reply("Correct Answer")
            else:
                logger.debug("got correct user and incorrect answer, removing points from user {}".format(user))
                points.trivia_correct_answer(inter.id, inter.author.id, inter.guild.id,
                                      self.difficulty_scale[question.difficulty] * -1)
                await inter.response.reply("Wrong Answer. It was {}".format(html.unescape(question.answers[question.correct_index])))


        except asyncio.TimeoutError:
            await inter.response.reply("Took too long to answer")


def setup(bot):
    return bot.add_cog(Trivia(bot))
