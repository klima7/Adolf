from os import environ
import requests
import json
from enum import Enum, auto
from app.translate import translate


_AUTH_HEADER = {'x-api-key': environ.get('CATS_API_KEY')}


class CatType(Enum):
    STATIC = auto()
    GIF = auto()

    @property
    def api_val(self):
        if self.name == 'STATIC':
            return 'jpg,png'
        if self.name == 'GIF':
            return 'gif'


class CatCategory(Enum):
    BOXES = 5
    CLOTHES = 15
    HATS = 1
    SINKS = 14
    SPACE = 2
    SUNGLASSES = 4
    TIES = 7

    @property
    def api_val(self):
        return str(self.value)


class CatBreed:

    def __init__(self, id_, name, description):
        self.id = id_
        self.name = name
        self.description = description

    def __repr__(self):
        return f'CatBreed[id={self.id}, name={self.name}]'

    @property
    def translated_name(self):
        return translate(self.name, 'en', 'pl')

    @property
    def translated_description(self):
        return translate(self.description, 'en', 'pl')

    @classmethod
    def get_cats_breeds(cls):
        res = requests.get(f'https://api.thecatapi.com/v1/breeds', headers=_AUTH_HEADER)
        breeds_dict = json.loads(res.content.decode('utf-8-sig'))
        breeds = [cls(breed['id'], breed['name'], breed['description']) for breed in breeds_dict]
        return breeds


CatBreed.breeds = CatBreed.get_cats_breeds()


def get_random_cats(count=1, type=None, category=None, breed=None):
    params = {'limit': count}
    if category is not None:
        params['category_ids'] = category.api_val
    if type is not None:
        params['mime_types'] = type.api_val
    if breed is not None:
        params['breed_ids'] = breed.id

    res = requests.get(f'https://api.thecatapi.com/v1/images/search', headers=_AUTH_HEADER, params=params)
    cats = json.loads(res.content.decode('utf-8-sig'))
    return [cat['url'] for cat in cats]


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    #print(breeds[:10])
    print(CatBreed.breeds)








