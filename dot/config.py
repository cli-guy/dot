import os
import sys
import json

class Config(object):
    has_file = False
    def __init__(self, file=None, start=None, from_env=False):
        if file:
            Config.file_path = file
            Config.has_file  = True

        self._load()

        if start:
            self.update(start)
        
        if from_env:
            self.parse_env()

    def __getattr__(self, name):
        return self.__dict__.get(name)

    def __setattr__(self, name , value):
        self.__dict__[name] = value
        self._save()
    
    def set_file(self, path):
        Config.file_path = path
        Config.has_file = True

    def rm(self, name):
        self.__dict__.pop(name, None)
        self._save()

    def ls(self):
        return list(self.__dict__.keys())

    def update(self, value):
        self.__dict__.update(value)
        self._save()

    def parse_env(self):
        for key in self.ls():
            if self.__dict__[key] == 'FROM_ENV':
                self.__dict__[key] = os.environ.get(key.upper(), 'NOT_SET')

    def _load(self):
        if Config.has_file:
            try:
                with open(Config.file_path, 'r') as file:
                    self.__dict__.update(json.loads(file.read()))
            except (json.JSONDecodeError, FileNotFoundError) as e:
                sys.exit('File not found', Config.file_path)

    def _save(self):
        if Config.has_file:
            try:
                with open(Config.file_path, 'w') as file:
                    file.write(json.dumps(self.__dict__,sort_keys=True, indent=2))
            except Exception as e:
                print(e)

