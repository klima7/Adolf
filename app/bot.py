import time
from os import environ

import fbchat as fb
from dotenv import load_dotenv

from app.jbzd import fetch_memes_page


class CustomClient(fb.Client):
    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        if not author_id == target_user.uid or not thread_type == fb.ThreadType.USER:
            return

        if message_object.text.lower().startswith('kocham ci'):
            time.sleep(5)
            client.sendMessage("Ja Ciebie też ;*", thread_id=thread_id)
            client.send(fb.Message(text="❤", emoji_size=fb.EmojiSize.LARGE), thread_id=thread_id)

        elif message_object.text.lower().startswith('meow'):
            client.sendMessage("Meow... 😺", thread_id=thread_id)

        elif message_object.text.lower().startswith('kici kici'):
            client.sendMessage("Mrrrr... 😺", thread_id=thread_id)

        elif message_object.text.lower().startswith('psik'):
            client.sendMessage("Meow?... 😿", thread_id=thread_id)


load_dotenv()
client = CustomClient(environ.get('MESSENGER_LOGIN'), environ.get('MESSENGER_PASSWORD'))
target_user = client.searchForUsers(environ.get('MESSENGER_TARGET'))[0]

memes = fetch_memes_page(1)
print(memes)
client.sendRemoteFiles(memes, thread_id=target_user.uid)
client.listen()
