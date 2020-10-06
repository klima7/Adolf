import inspect
import logging
import threading
import re
from os import environ
from random import choice, randint

import fbchat as fb

from app.memory import MemoryMixin
import app.util.jbzd as jbzd
from app.texts import texts
from app.policy import *


ELITE_GROUP_ID = environ.get('MESSENGER_THREAD_UID')

logger = logging.getLogger('logger')
registered_regex = {}
registered_actions = {}


def repeal(fun):
    def do_nothing(*args, **kwargs):
        pass
    return do_nothing


def elite_group_only(fun):
    def fake_fun(*args, **kwargs):
        matched_args = inspect.getcallargs(fun, *args, **kwargs)
        self = matched_args['self']
        thread_id = matched_args['thread_id']
        thread_type = matched_args.get('thread_type', fb.ThreadType.GROUP)
        author_id = matched_args['author_id']

        if author_id == self.uid:
            return
        if thread_id == ELITE_GROUP_ID:
            fun(*args, **kwargs)
        elif thread_type == fb.ThreadType.USER:
            self.meow_stranger(thread_id, thread_type)
    return fake_fun


def register_regex(regex):
    def real_decorator(fun):
        print('registering', fun.__name__)
        compiled_re = re.compile(regex, re.IGNORECASE)
        registered_regex[compiled_re] = fun
        return fun
    return real_decorator


class AdolfBot(fb.Client, MemoryMixin):

    # Attributes required by MemoryMixin
    MEMORY_DEFAULT = {'memes_page': 1}
    MEMORY_PATH = 'resources/memory.ini'

    PETTING_REQUIRED = 6
    TIME_CONSTANT = 10

    MAX_MARGIN = 60*6
    MAX_POOPY = 10*60*6
    MAX_HUNGER = 9*60*6
    MAX_THIRST = 7*60*6
    MAX_BOREDOM = 6*60*6

    HEARTS_COUNT = 6
    WANT_CHANCE = 10

    def __init__(self, mail, password):
        fb.Client.__init__(self, mail, password, logging_level=logging.WARNING)
        MemoryMixin.__init__(self)

        # state
        self.actions = []
        self.petting_counter = 5
        self.emoji = '👋'

        # stats
        self.stats = {
            Needs.HUNGER: self.MAX_HUNGER // 2,
            Needs.THIRST: self.MAX_THIRST // 2,
            Needs.POOPY: self.MAX_POOPY // 2,
            Needs.BOREDOM: self.MAX_BOREDOM // 2
        }

        self.change_emoji(self.emoji)
        self.time_loop()

    # ------------------------------------------- overloaded methods -----------------------------------------

    @repeal
    def onLoggedIn(self, email=None):
        self.hello_after_absence()

    def onFriendRequest(self, from_id=None, msg=None):
        self.sendMessage("Ktoś chce dodać mnie do znajomych", thread_id=environ.get('MESSENGER_THREAD_UID'), thread_type=fb.ThreadType.GROUP)

    @elite_group_only
    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        logger.info(f'Message received: {message_object.text} ({self.get_name(author_id)})')

        for (regex, callback) in registered_regex.items():
            if regex.search(message_object.text):
                should_return = callback(self, message_object.text, author_id, thread_id, thread_type)
                if should_return:
                    return

    def onTyping(self, author_id=None, status=None, thread_id=None, thread_type=None, msg=None):
        if thread_id != ELITE_GROUP_ID:
            return

        if self.actions and self.actions[-1] == Action.PETTING:
            if status == fb.TypingStatus.TYPING:
                response = texts.happy_cat_sound + '😺'
                self.sendMessage(response, thread_id=thread_id, thread_type=thread_type)
                self.petting_counter -= 1
                if self.petting_counter <= 0:
                    del self.actions[-1]
                    self.sendMessage(texts.thanks_petting, thread_id=thread_id, thread_type=thread_type)
            elif status == fb.TypingStatus.STOPPED:
                self.sendMessage(texts.stop_petting, thread_id=thread_id, thread_type=thread_type)

    @elite_group_only
    def onEmojiChange(self, mid=None, author_id=None, new_emoji=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None):
        if new_emoji != self.emoji:
            self.sendMessage(texts.dont_change_emoji, thread_id=thread_id, thread_type=fb.ThreadType.GROUP)
            self.changeThreadEmoji(self.emoji, thread_id)

    @elite_group_only
    def onTitleChange(self, mid=None, author_id=None, new_title=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None,):
        self.sendMessage("Nie zmieniaj Tytułu 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @elite_group_only
    def onImageChange(self, mid=None, author_id=None, new_image=None, thread_id=None,
                      thread_type=fb.ThreadType.GROUP, ts=None, msg=None,):
        self.sendMessage("Nie zmieniaj zdjęcia 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @elite_group_only
    def onColorChange(self, mid=None, author_id=None, new_color=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None):
        self.sendMessage("Jaki łady kolor 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @elite_group_only
    def onNicknameChange(self, mid=None, author_id=None, changed_for=None, new_nickname=None, thread_id=None,
                         thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None,):
        self.sendMessage("Nie zmieniaj pseudonomów 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @elite_group_only
    def onPeopleAdded(self, mid=None, added_ids=None, author_id=None, thread_id=None, ts=None, msg=None):
        self.sendMessage("Nie dodawaj nieznajomych do grupy 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @elite_group_only
    def onPersonRemoved(self, mid=None, removed_id=None, author_id=None, thread_id=None, ts=None, msg=None):
        self.sendMessage("I nie ma XD", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @elite_group_only
    def onReactionAdded(self, mid=None, reaction=None, author_id=None, thread_id=None,
                        thread_type=None, ts=None, msg=None):
        self.sendMessage("Dodałeś reakcję 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @elite_group_only
    def onPollCreated(self, mid=None, poll=None, author_id=None, thread_id=None,
                      thread_type=None, ts=None, metadata=None, msg=None):
        self.sendMessage("Oo, ankieta 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)
        option = choice(poll.options)
        self.updatePollVote(poll.uid, option_ids=[option.uid])
        self.sendMessage(f"{option.text}! Zdecydowanie 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    # ------------------------------------------- own methods -----------------------------------------

    def change_emoji(self, emoji):
        self.emoji = emoji
        self.changeThreadEmoji(emoji, ELITE_GROUP_ID)

    def hello_after_absence(self):
        self.sendMessage("Już wróciłem, meow, meow😽 Nie było mnie przez chwilkę😸", thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)

    def meow_stranger(self, thread_id, thread_type):
        if thread_type == fb.ThreadType.USER:
            self.sendMessage("Meow...", thread_id=thread_id, thread_type=thread_type)

    def get_name(self, uid):
        return self.fetchUserInfo(uid)[uid].first_name

    def time_loop(self):
        self.update_state()
        threading.Timer(AdolfBot.TIME_CONSTANT, self.time_loop).start()

    def update_state(self):
        self.stats[Needs.HUNGER] -= 1
        self.stats[Needs.THIRST] -= 1
        self.stats[Needs.POOPY] -= 1
        self.stats[Needs.BOREDOM] -= 1

        if self.stats[Needs.HUNGER] == 0:
            self.sendMessage(texts.meal_need, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        elif self.stats[Needs.THIRST] == 0:
            self.sendMessage(texts.drink_need, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        elif self.stats[Needs.BOREDOM] == 0:
            self.sendMessage(texts.toy_need, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        elif self.stats[Needs.POOPY] == 0:
            self.sendMessage(texts.poopy_need, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)

    @staticmethod
    def _get_stats_hearts(value, max_):
        count = round(AdolfBot.HEARTS_COUNT * value / max_)
        return '❤'*count + '🖤' * (AdolfBot.HEARTS_COUNT-count)


import app.regex







