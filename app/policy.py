from collections import namedtuple
from enum import Enum, IntEnum, auto
from os import environ

ELITE_GROUP_ID = environ.get('MESSENGER_THREAD_UID')
PETTING_COUNT_REQUIRED = 6
TIME_UPDATE_INTERVAL = 10

ENOUGH_MARGIN = 60 * 6
MAX_POOPY_VALUE = 10 * 60 * 6
MAX_HUNGER_VALUE = 9 * 60 * 6
MAX_THIRST_VALUE = 7 * 60 * 6
MAX_BOREDOM_VALUE = 6 * 60 * 6

STAT_HEARTS_COUNT = 6
STAT_POSITIVE_CHARACTER = '❤'
STAT_NEGATIVE_CHARACTER = '🖤'
EATING_WILLINGNESS = 10

something = namedtuple('something', 'name value')

meals = {
    '🍓': something('truskaweczkę', 800),
    '🍤': something('krewetkę', 400),
    '🥓': something('bekon', 500),
    '🐁': something('myszkę', 600),
    '🍣': something('suszi', 800),
    '🐀': something('szczura', 1000),
    '🐟': something('rybkę', 1200),
    '🍗': something('wołowine', 1300),
    '🥩': something('stek', 1500),
    '🍖': something('mięso z kością', 1700) #6h
}

drinks = {
    '💧': something('wodę', 300),
    '💦': something('kropelki wody', 600),
    '🥛': something('mleczko', 1000),
    '🍸': something('drinka', 1300),
    '🍼': something('mleczko w butelce', 1700),
}

toys = {
    '📿': something('naszyjnikiem', 300),
    '🎉': something('kolorowymi wstążeczkami', 800),
    '🎏': something('rybkami', 900),
    '🧶': something('włóczką', 1200)
}


class Action(Enum):
    PETTING = auto()


class Needs(IntEnum):
    HUNGER = auto()
    THIRST = auto()
    POOPY = auto()
    BOREDOM = auto()
