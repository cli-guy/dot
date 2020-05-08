#!/usr/bin/env python3
"""Usage:
"""

__version__ = '1.0'

import os
import sh
import sys
import shutil
import datetime
from dot.config import Config


class Dot(object):
    def __init__(self):
        self.cfg = Config(start={'home': 'FROM_ENV'}, from_env=True)
        self.cfg.set_file(os.path.join(self.cfg.home, '.dot'))
        self.cfg.old_dotfiles = os.path.join(self.cfg.home, ".old_dotfiles")
        self.cfg._input('username', 'What\'s your full name for git')
        self.cfg._input('repo', 'What\'s your git repository url')
        self.cfg._input('email', 'What\'s your email')
        self.args = sys.argv[1:]
        self.git_commands = ['add','am','apply','archive','bisect','blame','branch','bundle','cherry','cherry-pick','citool','clean','clone','commit','config','describe','diff','difftool','fetch','format-patch','fsck','gc','gitk','grep','gui','help','init','instaweb','log', 'ls-tree', 'merge','mergetool','mv','notes','pull','push','range-diff','rebase','reflog','remote','repack','replace','request-pull','reset','revert','rm','send-email','shortlog','show','show-branch','stage','stash','status','submodule','tag','whatchanged','worktree',]
        self.git = sh.git.bake(f"--git-dir={os.path.join(self.cfg.home, '.cfg')}",  f"--work-tree={self.cfg.home}", "-c", f"user.name={self.cfg.username}", "-c", f"user.email={self.cfg.email}")
        self.commands = ['status', 'load', 'save', 'ls']
        self.check_create_repo()
        if len(self.args) > 0 and self.args[0] in self.commands:
           self.__getattribute__(self.args[0])()
        elif len(self.args) > 0 and self.args[0] in self.git_commands:
            print(self.git(*self.args))
        else:
            self.status()

    def check_create_repo(self):
        if not os.path.exists(os.path.join(self.cfg.home, ".cfg")):
            with open(os.path.join(self.cfg.home, '.gitignore'), 'w') as file:
                file.write(".cfg")
            clone = self.git(f"git clone --bare {self.cfg.repo} {os.path.join(self.cfg.home, '.cfg')} --verbose")
            if clone.exit_code == 0:
                self.git('config', '--local', 'status.showUntrackedFiles', 'no')

    def status(self):
        print(self.git.status())

    def revert(self):
        sh.rm('-r', f'{self.cfg.home}/.gitignore', f'{self.cfg.home}/.cfg')

    def load(self):
        checkout = self.git.checkout()
        if checkout.exit_code == 0:
            print('Load completed.')
        else:
            output = checkout.stderr.split("checkout:\n")[1].split("\nPlease move or")[0].replace('\t', "")
            print(f"The following files need to be moved \n\n{output}")
            if input('\nType yes to move them to .old_dotfiles or move then yourself and run checkout again: ') == 'yes':
                if not os.path.exists(self.cfg.old_dotfiles):
                    print('Creating .old_files')
                    os.mkdir(self.cfg.old_dotfiles)
                for f in output.split('\n'):
                    file_dir = os.path.split(f)[0]
                    if len(file_dir) > 0 and not os.path.exists(os.path.join(self.cfg.old_dotfiles, file_dir)):
                        os.makedirs(os.path.join(self.cfg.old_dotfiles, os.path.split(f)[0]))
                    shutil.move(os.path.join(self.cfg.home, f), os.path.join(self.cfg.old_dotfiles, f))
                self.load()

    def save(self):
        status = self.git.status().split('\n')
        if status[1].startswith("Changes"):
            status = [x.replace('\t', '') for x in status[3:-3]]
            print("\n".join(status))
            self.git.commit("-a", "-m", str(datetime.datetime.now()))
            self.git.push("origin", "master")

    def ls(self):
        print('Files currently being tracked by dot:')
        print(self.git("ls-tree", "master", "--name-only", "--full-tree", "-r"))


def main():
    Dot()

if __name__ == '__main__':
    main()

