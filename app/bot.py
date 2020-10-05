import inspect
from os import environ
from random import choice

import fbchat as fb

from app.memory import MemoryMixin

ELITE_GROUP_ID = environ.get('MESSENGER_THREAD_UID')


class AdolfBot(fb.Client, MemoryMixin):

    # Attributes required by MemoryMixin
    MEMORY_DEFAULT = {'val': 7}
    MEMORY_PATH = 'resources/memory.ini'

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

    # ------------------------------------------- overloaded methods -----------------------------------------

    def onLoggedIn(self, email=None):
        pass
        self.hello_after_absence()

    def onFriendRequest(self, from_id=None, msg=None):
        self.sendMessage("Ktoś chce dodać mnie do znajomych", thread_id=environ.get('MESSENGER_THREAD_UID'), thread_type=fb.ThreadType.GROUP)

    @elite_group_only
    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        self.sendMessage("Mrau...", thread_id=thread_id, thread_type=thread_type)

    @elite_group_only
    def onEmojiChange(self, mid=None, author_id=None, new_emoji=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None):
        self.sendMessage("Nie zmieniaj Emoji 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

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

    @elite_group_only
    def onLiveLocation(self, mid=None, location=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):
        # Sends message three times every location sharing (1 on start, 2 on close)
        self.sendMessage(f"Oo, jesteś w {location.latitude}, {location.longitude}😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    # ------------------------------------------- own methods -----------------------------------------

    def hello_after_absence(self):
        self.sendMessage("Już wróciłem, meow, meow😽 Nie było mnie przez chwilkę😸", thread_id=ELITE_GROUP_ID, thread_type=fb.ThreadType.GROUP)

    def meow_stranger(self, thread_id, thread_type):
        if thread_type == fb.ThreadType.USER:
            self.sendMessage("Meow...", thread_id=thread_id, thread_type=thread_type)


