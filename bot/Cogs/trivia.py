import asyncio
import disnake
from disnake.ext import commands
import requests
import logging
import random
import datetime
from utils.query import *
from utils.points import *
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
        self.emoji_to_index = {'A': 0,
                               'B': 1,
                               'C': 2,
                               'D': 3}
        self.difficulty_scale = {'easy': 2, "medium": 4, "hard": 6}
        self.question = 0

    def cool_down(self, author_id, guild_id):
        logging.debug("starting cooldown check for user: {0} in guild: {1}".format(author_id, guild_id))
        last_post_time = trivia_cooldown(author_id, guild_id)
        if last_post_time is None:
            return False
        now = datetime.datetime.now()
        diff_time = (now - last_post_time).seconds / 60.0
        logger.info("{0} minutes since last post from user: {1}".format(diff_time, author_id))
        if diff_time < 5.0:
            return True
        else:
            return False

    def get_question(self):
        logger.info("getting trivia answer from api")
        trivia_url = random.choice(self.trivia_urls)
        if trivia_url['category'] is None:
            trivia_url['category'] = ''
        if trivia_url['difficulty'] is None:
            trivia_url['difficulty'] = ''
        print(trivia_url['url'])
        res = requests.get(trivia_url['url'])
        logger.info('Got request from trivia api: {}'.format(res))
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
        logger.info("starting trivia command")
        if self.cool_down(inter.author.id, inter.guild.id):
            logger.info("trvia debug 0")
            await inter.response.send_message("On cooldown")
            logger.info("trvia debug 1")
            return
        logger.info("trvia debug 2")
        await inter.response.defer()
        self.question = self.get_question()
        logger.info("trvia debug 3")
        embed = self.create_message(self.question)
        logger.info("trvia debug 4")
        view = TriviaButtons()
        message = await inter.channel.send(embed=embed, view=view)
        logger.info("trvia debug 5")

        await view.wait()
        for child in view.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True
        await message.edit(view=view)

        if view.value == self.question.correct_index:
            logger.info("Got correct answer. Awarding points")
            trivia_correct_answer(inter.id, inter.author.id, inter.guild.id,
                                           self.difficulty_scale[self.question.difficulty])
            await inter.channel.send("Correct answer. You earned" + str(self.difficulty_scale[self.question.difficulty]) + " points")
            await inter.edit_original_response(content="Received Answer")
        else:
            logger.info("Got wrong answer. Removing points")
            trivia_correct_answer(inter.id, inter.author.id, inter.guild.id, self.difficulty_scale[self.question.difficulty] * -1)
            await inter.channel.send("Incorrect answer. You lost "+ str(self.difficulty_scale[self.question.difficulty]) + " points")
            await inter.edit_original_response(content="Received Answer")


class TriviaButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=10.0)
        self.value = None

    @disnake.ui.button(label='A', style=disnake.ButtonStyle.primary)
    async def a_hit(self, button, inter):
        await inter.response.send_message("Input Received...", ephemeral=True)
        self.value = 0
        self.stop()

    @disnake.ui.button(label='B', style=disnake.ButtonStyle.primary)
    async def b_hit(self, button, inter):
        await inter.response.send_message("Input Received...", ephemeral=True)
        self.value = 1
        self.stop()

    @disnake.ui.button(label='C', style=disnake.ButtonStyle.primary)
    async def c_hit(self, button, inter):
        await inter.response.send_message("Input Received...", ephemeral=True)
        self.value = 2
        self.stop()

    @disnake.ui.button(label='D', style=disnake.ButtonStyle.primary)
    async def d_hit(self, button, inter):
        await inter.response.send_message("Input Received...", ephemeral=True)
        self.value = 3
        self.stop()

def setup(bot):
    return bot.add_cog(Trivia(bot))
