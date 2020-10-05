from os import environ

from app.client import AdolfClient


client = AdolfClient()
client.login(environ.get('MESSENGER_LOGIN'), environ.get('MESSENGER_PASSWORD'))
client.listen()
