from typing import Any, List
import yaml

from highlight_butler.utils.singleton import Singleton

class Config(metaclass=Singleton):
    def __init__(self):
        self.config = {}
    
    def load(self, config_data):
        try:
            self.config = yaml.full_load(config_data)
        except Exception as e:
            print(e)
    
    def get_value(self, query: Any, default=None):
        value = self.config
        if type(query) == str:
            query = query.split(".")
        while len(query) > 0:
            k = query.pop(0)
            value = value.get(k)
            if value == None:
                return default
            
        return value