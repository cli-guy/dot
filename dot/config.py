import os
import sys
import json
from pathlib import Path

class Config(dict):
    """Config Object"""
    def __init__(self, docstring):
        self.docstring = docstring
        self.home = str(Path.home())
        self.location = os.path.join(self.home, '.dot')
        self.required = {
            'repo': 'Please enter the git repo url for your dot files: ',
            'username': 'Please enter your git username:' ,
            'email': 'Please enter your git user email address: '
        }
        self.map = {
            "--url" : "repo",
            "--user": "username",
            "--email": "email"
        }
        __getattr__ = dict.get
        __delattr__ = dict.__delitem__
        self._load()

    def _parse_options(self):
        for key in self.map.keys():
            if key in self.args:
                self.__setattr__(self.map[key], self.args[self.args.index(key)+1], save=True)

    def __setattr__(self, name, value, save=False):
        entry = {name: value}
        self.__dict__.update(entry)
        if save:
            self.file.update(entry)
            self._save()

    def _load(self):
        try:
            with open(self.location, 'r') as file:
                self.file = json.loads(file.read())
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.file = {}
        self.__dict__.update(self.file)
        self.args = sys.argv[1:]
        if len(self.args) > 0 and self.args[0] == 'init':
            self._parse_options()
        for value in self.required:
            if value not in self.__dict__.keys():
                self.__setattr__(value, str(input(self.required[value])), save=True)

    def _save(self):
        with open(self.location, 'w') as file:
            file.write(json.dumps(self.file, indent=2))


