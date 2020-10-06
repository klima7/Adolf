from app.bot import register_regex, ELITE_GROUP_ID, AdolfBot
import fbchat as fb
from random import randint
from app.texts import texts
from app.policy import *
from app.util import jbzd


@register_regex("jak tam?")
def reply_stats(self, message, author_id, thread_id, thread_type):
    response = 'Jedzonko: {}\nPićko       : {}\nZabawa   : {}\nKupka      : {}'.format(
        self._get_stats_hearts(self.stats[Needs.HUNGER], self.MAX_HUNGER),
        self._get_stats_hearts(self.stats[Needs.THIRST], self.MAX_THIRST),
        self._get_stats_hearts(self.stats[Needs.BOREDOM], self.MAX_BOREDOM),
        self._get_stats_hearts(self.stats[Needs.POOPY], self.MAX_POOPY))
    self.sendMessage(response, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)


@register_regex(f"^{'|'.join(meals.keys())}$")
def reply_meal(self, message, author_id, thread_id, thread_type):
    if self.stats[Needs.HUNGER] + self.MAX_MARGIN > self.MAX_HUNGER:
        self.sendMessage(texts.meal_enough, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    if randint(0, self.WANT_CHANCE) == 0:
        self.sendMessage(texts.dont_want.format(meals[message].name), thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    value = meals[message].value
    self.sendMessage(texts.meal_good, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    if self.stats[Needs.HUNGER] < 0: self.stats[Needs.HUNGER] = value
    else: self.stats[Needs.HUNGER] = min(self.stats[Needs.HUNGER] + value, self.MAX_HUNGER)


@register_regex(f"^{'|'.join(drinks.keys())}$")
def reply_drink(self, message, author_id, thread_id, thread_type):
    if self.stats[Needs.THIRST] + self.MAX_MARGIN > self.MAX_THIRST:
        self.sendMessage(texts.drink_enough, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    if randint(0, self.WANT_CHANCE) == 0:
        self.sendMessage(texts.dont_want.format(drinks[message].name), thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    value = drinks[message].value
    self.sendMessage(texts.drink_good, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    if self.stats[Needs.THIRST] < 0: self.stats[Needs.THIRST] = value
    else: self.stats[Needs.THIRST] = min(self.stats[Needs.THIRST] + value, self.MAX_THIRST)


@register_regex(f"^{'|'.join(toys.keys())}$")
def reply_toy(self, message, author_id, thread_id, thread_type):
    if self.stats[Needs.BOREDOM] + self.MAX_MARGIN > self.MAX_BOREDOM:
        self.sendMessage(texts.toy_enough, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    if randint(0, self.WANT_CHANCE) == 0:
        self.sendMessage(texts.dont_want.format('zabawę ' + toys[message].name), thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    value = toys[message].value
    self.sendMessage(texts.toy_good, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    if self.stats[Needs.BOREDOM] < 0: self.stats[Needs.BOREDOM] = value
    else: self.stats[Needs.BOREDOM] = min(self.stats[Needs.BOREDOM] + value, self.MAX_BOREDOM)


@register_regex(f"^🚽$")
def reply_poopy(self, message, author_id, thread_id, thread_type):
    if self.stats[Needs.POOPY] + self.MAX_MARGIN > self.MAX_POOPY:
        self.sendMessage(texts.poopy_enough, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        return
    self.sendMessage(texts.poopy_good, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
    self.stats[Needs.POOPY] = self.MAX_POOPY


@register_regex(r'\bkocham\b')
def reply_love_you(self, message, author_id, thread_id, thread_type):
    self.sendMessage(f"Też Cię kocham {self.get_name(author_id)}", thread_id=thread_id, thread_type=thread_type)


@register_regex(r'\bmemy\b')
def reply_memy(self, message, author_id, thread_id, thread_type):
    self.sendMessage("Mrauu, oto świeżutkie memy dla Ciebie 😼👇", thread_id=thread_id, thread_type=thread_type)
    memes = jbzd.fetch_memes_page(1)
    self['memes_page'] = 2
    memes_url = [meme.url for meme in memes]
    self.sendRemoteFiles(memes_url, thread_id=thread_id, thread_type=thread_type)
    self.sendMessage("Chcecie więcej? ", thread_id=thread_id, thread_type=thread_type)


@register_regex(r'\bta+k\b')
def reply_tak(self, message, author_id, thread_id, thread_type):
    self.sendMessage("Dobrze, zaraz wyślę 😹", thread_id=thread_id, thread_type=thread_type)
    memes = jbzd.fetch_memes_page(self['memes_page'])
    self['memes_page'] = int(self['memes_page']) + 1
    memes_url = [meme.url for meme in memes]
    self.sendRemoteFiles(memes_url, thread_id=thread_id, thread_type=thread_type)
    self.sendMessage("Jeszcze więcej? 🙀", thread_id=thread_id, thread_type=thread_type)


@register_regex(r'\bgłaskanie\b|^👋$')
def reply_petting(self, message, author_id, thread_id, thread_type):
    self.sendMessage(texts.start_petting, thread_id=thread_id, thread_type=thread_type)
    self.petting_counter = AdolfBot.PETTING_REQUIRED
    self.actions.append(Action.PETTING)
