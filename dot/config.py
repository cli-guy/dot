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
            self._update(start)
        if from_env:
            self._parse_env()

    def __getattr__(self, name):
        return self.__dict__.get(name)

    def __setattr__(self, name , value):
        self.__dict__[name] = value
        self._save()
    
    def set_file(self, path):
        Config.file_path = path
        Config.has_file = True
        self._load()

    def _rm(self, name):
        self.__dict__.pop(name, None)
        self._save()

    def _ls(self):
        return list(self.__dict__.keys())

    def _update(self, value):
        self.__dict__.update(value)
        self._save()

    def _input(self, name, question):
        if name not in self._ls():
            self.__setattr__(name, input(f"{question}: "))
        
    def _parse_env(self):
        for key in self._ls():
            if self.__dict__[key] == 'FROM_ENV':
                self.__dict__[key] = os.environ.get(key.upper(), 'NOT_SET')

    def _load(self):
        if Config.has_file:
            try:
                with open(Config.file_path, 'r') as file:
                    self.__dict__.update(json.loads(file.read()))
            except FileNotFoundError as e:
                sys.exit('File not found', Config.file_path)
            except json.JSONDecodeError as e:
                sys.exit('Error parsing json ', e)

    def _save(self):
        if Config.has_file:
            try:
                with open(Config.file_path, 'w') as file:
                    file.write(json.dumps(self.__dict__,sort_keys=True, indent=2))
            except Exception as e:
                print(e)

