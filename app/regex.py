import app.decorators as decorators
import fbchat as fb
from random import randint
from app.texts import texts
from app.policy import *
from app.util import jbzd
from app.memory import memory
import app.util.cats as cats


@decorators.register_regex("jak tam?")
def reply_stats(bot, message, author_id, thread_id, thread_type):
    response = 'Jedzonko: {}\nPićko       : {}\nZabawa   : {}\nKupka      : {}'.format(
        bot.get_stats_hearts(memory.hunger, MAX_HUNGER_VALUE),
        bot.get_stats_hearts(memory.thirst, MAX_THIRST_VALUE),
        bot.get_stats_hearts(memory.boredom, MAX_BOREDOM_VALUE),
        bot.get_stats_hearts(memory.poopy, MAX_POOPY_VALUE))
    bot.sendMessage(response, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)


@decorators.register_regex(f"^{'|'.join(meals.keys())}$")
def reply_meal(bot, message, author_id, thread_id, thread_type):
    if memory.hunger + ENOUGH_MARGIN > MAX_HUNGER_VALUE:
        bot.sendMessage(texts.meal_enough, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    if randint(0, EATING_WILLINGNESS) == 0:
        bot.sendMessage(texts.dont_want.format(meals[message].name), thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    value = meals[message].value
    bot.sendMessage(texts.meal_good, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    if memory.hunger < 0: memory.hunger = value
    else: memory.hunger = min(memory.hunger + value, MAX_HUNGER_VALUE)


@decorators.register_regex(f"^{'|'.join(drinks.keys())}$")
def reply_drink(bot, message, author_id, thread_id, thread_type):
    if memory.thirst + ENOUGH_MARGIN > MAX_THIRST_VALUE:
        bot.sendMessage(texts.drink_enough, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    if randint(0, EATING_WILLINGNESS) == 0:
        bot.sendMessage(texts.dont_want.format(drinks[message].name), thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    value = drinks[message].value
    bot.sendMessage(texts.drink_good, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    if memory.thirst < 0: memory.thirst = value
    else: memory.thirst = min(memory.thirst + value, MAX_THIRST_VALUE)


@decorators.register_regex(f"^{'|'.join(toys.keys())}$")
def reply_toy(bot, message, author_id, thread_id, thread_type):
    if memory.boredom + ENOUGH_MARGIN > MAX_BOREDOM_VALUE:
        bot.sendMessage(texts.toy_enough, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    if randint(0, EATING_WILLINGNESS) == 0:
        bot.sendMessage(texts.dont_want.format('zabawę ' + toys[message].name), thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    value = toys[message].value
    bot.sendMessage(texts.toy_good, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    if memory.boredom < 0: memory.boredom = value
    else: memory.boredom = min(memory.boredom + value, MAX_BOREDOM_VALUE)


@decorators.register_regex(f"^🚽$")
def reply_poopy(bot, message, author_id, thread_id, thread_type):
    if memory.poopy + ENOUGH_MARGIN > MAX_POOPY_VALUE:
        bot.sendMessage(texts.poopy_enough, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    bot.sendMessage(texts.poopy_good, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    memory.poopy = bot.MAX_POOPY_VALUE


@decorators.register_regex(r'\bkocham\b')
def reply_love_you(bot, message, author_id, thread_id, thread_type):
    bot.sendMessage(f"Też Cię kocham {bot.get_name(author_id)}", thread_id=thread_id, thread_type=thread_type)


@decorators.register_regex(r'\bmemy\b')
def reply_memy(bot, message, author_id, thread_id, thread_type):
    bot.sendMessage("Mrauu, oto świeżutkie memy dla Ciebie 😼👇", thread_id=thread_id, thread_type=thread_type)
    memes = jbzd.fetch_memes_page(1)
    memory.memes_page = 2
    memes_url = [meme.url for meme in memes]
    bot.sendRemoteFiles(memes_url, thread_id=thread_id, thread_type=thread_type)
    bot.sendMessage("Chcecie więcej? ", thread_id=thread_id, thread_type=thread_type)


@decorators.register_regex(r'\bta+k\b')
def reply_tak(bot, message, author_id, thread_id, thread_type):
    bot.sendMessage("Dobrze, zaraz wyślę 😹", thread_id=thread_id, thread_type=thread_type)
    memes = jbzd.fetch_memes_page(memory.memes_page)
    memory.memes_page = memory.memes_page + 1
    memes_url = [meme.url for meme in memes]
    bot.sendRemoteFiles(memes_url, thread_id=thread_id, thread_type=thread_type)
    bot.sendMessage("Jeszcze więcej? 🙀", thread_id=thread_id, thread_type=thread_type)


@decorators.register_regex(r'\bgłaskanie\b|^👋$')
def reply_petting(bot, message, author_id, thread_id, thread_type):
    bot.sendMessage(texts.start_petting, thread_id=thread_id, thread_type=thread_type)
    memory.petting_counter = PETTING_COUNT_REQUIRED
    memory.action = Action.PETTING


@decorators.register_regex(r'\bkotki\b|^👋$')
def reply_petting(bot, message, author_id, thread_id, thread_type):
    cats_url = cats.get_random_cats(6, type=cats.CatType.STATIC)
    bot.sendMessage("Kotki dla Ciebie 🐱🐱🐱", thread_id=thread_id, thread_type=thread_type)
    bot.sendRemoteFiles(cats_url, thread_id=thread_id, thread_type=thread_type)
