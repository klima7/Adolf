from os import environ

import fbchat as fb


class AdolfClient(fb.Client):

    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        if author_id == self.uid:
            return

        if thread_id == environ.get('MESSENGER_THREAD_UID'):
            self.sendMessage("Mrau...", thread_id=thread_id, thread_type=fb.ThreadType.GROUP)

        elif thread_type == fb.ThreadType.USER:
            self.sendMessage("Meow... 😺", thread_id=thread_id)
