import logging
from sys import stdout
from os import environ

from app.bot import AdolfBot


def create_logger():
    logger = logging.getLogger('logger')
    handler = logging.StreamHandler(stdout)
    formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
    handler.setFormatter(formater)
    handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


logger = create_logger()
client = AdolfBot(environ.get('MESSENGER_LOGIN'), environ.get('MESSENGER_PASSWORD'))
logger.info('Login success')

import app.events
import app.regex

client.listen()
