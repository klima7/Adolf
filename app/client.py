from os import environ
from random import choice

import fbchat as fb

from app.memory import MemoryMixin


class AdolfClient(fb.Client, MemoryMixin):

    MEMORY_DEFAULT = {'val': 7}
    MEMORY_PATH = 'resources/memory.ini'

    def __init__(self):
        try:
            fb.Client.__init__(self, '', '', max_tries=1)
        except fb.FBchatUserError:
            pass
        MemoryMixin.__init__(self)
        self.cat = None

    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        if author_id == self.uid:
            return

        if thread_id == environ.get('MESSENGER_THREAD_UID'):
            self.sendMessage("Mrau...", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

        elif thread_type == fb.ThreadType.USER:
            self.sendMessage("Meow... 😺", thread_id=thread_id)

    def onLoggedIn(self, email=None):
        pass
        self.hello_after_absence()
        # self.sendMessage("Nie było mnie przez chwilę, ale już wróciłem 😺", thread_id=environ.get('MESSENGER_THREAD_UID'), thread_type=fb.ThreadType.GROUP)

    def onEmojiChange(self, mid=None, author_id=None, new_emoji=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None):
        self.sendMessage("Nie zmieniaj Emoji 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onTitleChange(self, mid=None, author_id=None, new_title=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None,):
        self.sendMessage("Nie zmieniaj Tytułu 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onImageChange(self, mid=None, author_id=None, new_image=None, thread_id=None,
                      thread_type=fb.ThreadType.GROUP, ts=None, msg=None,):
        self.sendMessage("Nie zmieniaj zdjęcia 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onColorChange(self, mid=None, author_id=None, new_color=None, thread_id=None,
                      thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None):
        self.sendMessage("Jaki łady kolor 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onNicknameChange(self, mid=None, author_id=None, changed_for=None, new_nickname=None, thread_id=None,
                         thread_type=fb.ThreadType.USER, ts=None, metadata=None, msg=None,):
        self.sendMessage("Nie zmieniaj pseudonomów 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onMessageSeen(self, seen_by=None, thread_id=None, thread_type=fb.ThreadType.USER,
                      seen_ts=None, ts=None, metadata=None, msg=None,):
        # Warning: Repeating messages due to reading those newly send
        pass

    def onPeopleAdded(self, mid=None, added_ids=None, author_id=None, thread_id=None, ts=None, msg=None):
        self.sendMessage("Nie dodawaj nieznajomych do grupy 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onPersonRemoved(self, mid=None, removed_id=None, author_id=None, thread_id=None, ts=None, msg=None):
        self.sendMessage("I nie ma XD", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onFriendRequest(self, from_id=None, msg=None):
        self.sendMessage("Nie dodawaj nieznajomych do grupy 😿", thread_id=environ.get('MESSENGER_THREAD_UID'), thread_type=fb.ThreadType.GROUP)

    def onTyping(self, author_id=None, status=None, thread_id=None, thread_type=None, msg=None):
        return
        if status == fb.TypingStatus.TYPING:
            self.sendMessage("Widzę, że piszesz na klawiaturze 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)
        elif status == fb.TypingStatus.STOPPED:
            self.sendMessage("Przestałeś pisać 😿", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onReactionAdded(self, mid=None, reaction=None, author_id=None, thread_id=None,
                        thread_type=None, ts=None, msg=None):
        self.sendMessage("Dodałeś reakcję 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onCallEnded(self, mid=None, caller_id=None, is_video_call=None, call_duration=None, thread_id=None,
                    thread_type=None, ts=None, metadata=None, msg=None):
        self.sendMessage("Miło się rozmawiało 😺😺😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onCallStarted(self, mid=None, caller_id=None, is_video_call=None, thread_id=None,
                      thread_type=None, ts=None, metadata=None, msg=None):
        self.sendMessage("Miło się rozmawiało 😺😺😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onMessageError(self, exception=None, msg=None):
        self.sendMessage("Oj, wystąpił jakiś błąd 😿", thread_id=environ.get('MESSENGER_THREAD_UID'), thread_type=fb.ThreadType.GROUP)

    def onPollCreated(self, mid=None, poll=None, author_id=None, thread_id=None,
                      thread_type=None, ts=None, metadata=None, msg=None):
        self.sendMessage("Oo, ankieta 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)
        option = choice(poll.options)
        self.updatePollVote(poll.uid, option_ids=[option.uid])
        self.sendMessage(f"{option.text}! Zdecydowanie 😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def onLiveLocation(self, mid=None, location=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):
        # Sends message three times every location sharing (1 on start, 2 on close)
        self.sendMessage(f"Oo, jesteś w {location.latitude}, {location.longitude}😺", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

    def hello_after_absence(self):
        self.sendMessage("Mrau...", thread_id='3742696045797944', thread_type=fb.ThreadType.GROUP)


