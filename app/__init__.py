from os import environ

from app.bot import AdolfBot


client = AdolfBot(environ.get('MESSENGER_LOGIN'), environ.get('MESSENGER_PASSWORD'))
client.listen()
