from configparser import *


class Config:

    DEFAULT_CONFIG = {
            'turbo': 'False',
            'nextmemepage': 1,
            'last_meme_url': ''
        }

    CONFIGURATION_FILE_NAME = '../config.ini'

    def __init__(self):
        self.config = ConfigParser()
        self.config['DEFAULT'] = Config.DEFAULT_CONFIG
        self.config.read(Config.CONFIGURATION_FILE_NAME)
        self._remove_old_keys()
        self._write()

    def __getitem__(self, item):
        return self.config['DEFAULT'][item]

    def __setitem__(self, key, value):
        if key not in Config.DEFAULT_CONFIG:
            raise KeyError(f'Key {key} is invalid')
        self.config['DEFAULT'][key] = str(value)
        self._write()

    def _write(self):
        with open(Config.CONFIGURATION_FILE_NAME, 'w') as f:
            self.config.write(f)

    def _remove_old_keys(self):
        for key in list(self.config['DEFAULT']):
            if key not in Config.DEFAULT_CONFIG:
                del self.config['DEFAULT'][key]
        self._write()


config = Config()
