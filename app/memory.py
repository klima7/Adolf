from configparser import *


class MemoryMixin:

    def __init__(self):
        self.config = ConfigParser()
        self.config['DEFAULT'] = self.MEMORY_DEFAULT
        self.config.read(self.MEMORY_PATH)
        self._remove_old_keys()
        self._write()

    def __getitem__(self, item):
        if self._is_proper_key(item):
            return self.config['DEFAULT'][item]
        raise KeyError(f'Key {item} is not in memory')

    def __setitem__(self, key, value):
        if not self._is_proper_key(key):
            raise KeyError(f'Key {key} is not in memory')
        self.config['DEFAULT'][key] = str(value)
        self._write()

    def get_mem(self, key, type=str):
        return type(self[key])

    def _write(self):
        with open(self.MEMORY_PATH, 'w') as f:
            self.config.write(f)

    def _remove_old_keys(self):
        for key in list(self.config['DEFAULT']):
            if not self._is_proper_key(key):
                del self.config['DEFAULT'][key]
        self._write()

    def _is_proper_key(self, val):
        return val in [key.lower() for key in self.MEMORY_DEFAULT]

