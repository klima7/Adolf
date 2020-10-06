import shelve
from app.policy import *


class DefaultMemory:

    hunger = MAX_HUNGER_VALUE // 2
    thirst = MAX_THIRST_VALUE // 2
    poopy = MAX_POOPY_VALUE // 2
    boredom = MAX_BOREDOM_VALUE // 2

    action = None
    petting_counter = 0
    emoji = ''
    memes_page = 1


class Memory:
    def __init__(self, path):
        self.__dict__['data'] = shelve.open(path, 'c', writeback=False)

    def __setattr__(self, key, value):
        self.__dict__['data'][key] = value
        self.__dict__['data'].sync()

    def __getattr__(self, item):
        try:
            val = self.__dict__['data'][item]
        except KeyError:
            val = getattr(DefaultMemory, item)
        return val


memory = Memory('resources/memory.shelve')
