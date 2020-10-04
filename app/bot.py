from os import environ

from app.client import AdolfClient


def start_bot():
    client = AdolfClient(environ.get('MESSENGER_LOGIN'), environ.get('MESSENGER_PASSWORD'))
    client.listen()
