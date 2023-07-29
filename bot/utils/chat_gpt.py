import os
from dotenv import load_dotenv
import logging
import openai
import tiktoken
from .query import *

load_dotenv()
logger = logging.getLogger("gpt")
openai.api_key = os.getenv("CHATGPT_API_KEY")
ai_model = os.getenv("CHATGPT_MODEL")
encoding = tiktoken.encoding_for_model(ai_model)
token_limit = os.getenv("CHATGPT_TOKEN_LIMIT")
use_gpt = os.getenv("USE_GPT")


def gpt_enabled() -> bool:
    if use_gpt == "TRUE":
        return True
    else:
        return False


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_opening_message(guild_id):
    rules = get_behaviors(guild_id)
    content = "You are MemekingBot. At most, your responses will be 2-3 sentences."
    for rule in rules:
        content = content + rule.rule
    logger.info("This is the first message content: {}".format(content))
    return content


def prompt_once(prompt: str, guild_id: str) -> str:
    logger.info("Got prompt from user: {}", prompt)
    logger.info("Request will take this make tokens: {}", num_tokens_from_string(prompt))
    if num_tokens_from_string(prompt) > 1000:
        return "Prompt too long"
    try:
        opening_message = get_opening_message(guild_id)
        logger.info("sending first message to gpt: {}", opening_message)
        logger.info("sending prompt to gpt: {}", prompt)
        response = openai.ChatCompletion.create(
            model=ai_model,
            messages=[
                {"role": "system", "content": opening_message},
                {"role": "user", "content": prompt}
            ],
            temperature=1
        )
        logger.info("response from chatgpt: {}", response)
    except openai.error.APIError as e:
        logger.info("got exception: {}", e)
        return "Could not complete request, API is down"
    except openai.error.APIConnectionError as e:
        logger.info("got exception: {}", e)
        return "Could not complete request, API Connection error"
    except openai.error.RateLimitError as e:
        logger.info("got exception: {}", e)
        return "Could not complete request, Rate Limit Reached {},"

    return response['choices'][0]['message']['content']
