import logging
import threading
from random import choice

import fbchat as fb

import app.decorators as decorators
from app.memory import MemoryMixin
from app.policy import *
from app.texts import texts

logger = logging.getLogger('logger')


class AdolfBot(fb.Client, MemoryMixin):

    MEMORY_DEFAULT = {'memes_page': 1}
    MEMORY_PATH = 'resources/memory.ini'

    def __init__(self, mail, password):
        fb.Client.__init__(self, mail, password, logging_level=logging.WARNING)
        MemoryMixin.__init__(self)

        # state
        self.action = None
        self.petting_counter = 0
        self.emoji = ''

        # stats
        self.hunger = MAX_HUNGER_VALUE // 2
        self.thirst = MAX_THIRST_VALUE // 2
        self.poopy = MAX_POOPY_VALUE // 2
        self.boredom = MAX_BOREDOM_VALUE // 2

        self.change_emoji('👋')
        self.time_loop()

    # ------------------------------------------- overloaded methods -----------------------------------------

    @decorators.repeal
    def onLoggedIn(self, email=None):
        self.sendMessage("Już wróciłem, meow, meow😽 Nie było mnie przez chwilkę😸", thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)

    def onFriendRequest(self, from_id=None, msg=None):
        self.sendMessage("Ktoś chce dodać mnie do znajomych", thread_id=environ.get('MESSENGER_THREAD_UID'), thread_type=fb.ThreadType.GROUP)

    @decorators.elite_group_only
    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        logger.info(f'Message received: {message_object.text} ({self.get_name(author_id)})')

        for (regex, callback) in decorators.registered_regex.items():
            if regex.search(message_object.text):
                should_return = callback(self, message_object.text, author_id, thread_id, thread_type)
                if should_return:
                    return

    def onTyping(self, author_id=None, status=None, thread_id=None, thread_type=None, msg=None):
        if thread_id != ELITE_GROUP_ID:
            return

        if self.action == Action.PETTING:
            if status == fb.TypingStatus.TYPING:
                response = texts.happy_cat_sound + '😺'
                self.sendMessage(response, thread_id=thread_id, thread_type=thread_type)
                self.petting_counter -= 1
                if self.petting_counter <= 0:
                    self.action = None
                    self.sendMessage(texts.thanks_petting, thread_id=thread_id, thread_type=thread_type)
            elif status == fb.TypingStatus.STOPPED:
                self.sendMessage(texts.stop_petting, thread_id=thread_id, thread_type=thread_type)

    @decorators.elite_group_only
    def onEmojiChange(self, mid=None, author_id=None, new_emoji=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None):
        if new_emoji != self.emoji:
            self.sendMessage(texts.dont_change_emoji, thread_id=thread_id, thread_type=fb.ThreadType.GROUP)
            self.changeThreadEmoji(self.emoji, thread_id)

    @decorators.elite_group_only
    def onTitleChange(self, mid=None, author_id=None, new_title=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None,):
        self.sendMessage("Nie zmieniaj Tytułu 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @decorators.elite_group_only
    def onImageChange(self, mid=None, author_id=None, new_image=None, thread_id=None,
                      thread_type=fb.ThreadType.GROUP, ts=None, msg=None,):
        self.sendMessage("Nie zmieniaj zdjęcia 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @decorators.elite_group_only
    def onColorChange(self, mid=None, author_id=None, new_color=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None):
        self.sendMessage("Jaki łady kolor 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @decorators.elite_group_only
    def onNicknameChange(self, mid=None, author_id=None, changed_for=None, new_nickname=None, thread_id=None,
                         thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None,):
        self.sendMessage("Nie zmieniaj pseudonomów 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @decorators.elite_group_only
    def onPeopleAdded(self, mid=None, added_ids=None, author_id=None, thread_id=None, ts=None, msg=None):
        self.sendMessage("Nie dodawaj nieznajomych do grupy 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @decorators.elite_group_only
    def onPersonRemoved(self, mid=None, removed_id=None, author_id=None, thread_id=None, ts=None, msg=None):
        self.sendMessage("I nie ma XD", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @decorators.elite_group_only
    def onReactionAdded(self, mid=None, reaction=None, author_id=None, thread_id=None,
                        thread_type=None, ts=None, msg=None):
        self.sendMessage("Dodałeś reakcję 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    @decorators.elite_group_only
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

    def meow_stranger(self, thread_id, thread_type):
        if thread_type == fb.ThreadType.USER:
            self.sendMessage("Meow...", thread_id=thread_id, thread_type=thread_type)

    def get_name(self, uid):
        return self.fetchUserInfo(uid)[uid].first_name

    def time_loop(self):
        self.update_state()
        threading.Timer(TIME_UPDATE_INTERVAL, self.time_loop).start()

    def update_state(self):
        self.hunger -= 1
        self.thirst -= 1
        self.poopy -= 1
        self.boredom -= 1

        if self.hunger == 0:
            self.sendMessage(texts.meal_need, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        elif self.thirst == 0:
            self.sendMessage(texts.drink_need, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        elif self.boredom == 0:
            self.sendMessage(texts.toy_need, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)
        elif self.poopy == 0:
            self.sendMessage(texts.poopy_need, thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)

    @staticmethod
    def get_stats_hearts(value, max_):
        count = round(STAT_HEARTS_COUNT * value / max_)
        return STAT_POSITIVE_CHARACTER * count + STAT_NEGATIVE_CHARACTER * (STAT_HEARTS_COUNT - count)



