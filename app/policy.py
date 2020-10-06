from collections import namedtuple
from enum import Enum, IntEnum, auto

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
