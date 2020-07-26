#!/usr/bin/env python3
"""Usage:
"""

__version__ = '1.0'

import os
import sys
import shutil
from subprocess import run
from jpconfig import Config


class Dot(object):
    def __init__(self):
        self.args = sys.argv[1:]
        self.home  = os.environ['HOME']
        self.local = os.path.join(self.home, '.cfg')
        self.old_dotfiles = os.path.join(self.home, ".old_dotfiles")
        self.cfg   = Config(file=os.path.join(self.home, '.dot'))
        if len(self.args) > 0 and self.args[0] == 'init':
            self.cfg.username = input('What\'s your full name for git')
            self.cfg.remote = input('What\'s your git repository url')
            self.cfg.email = input('What\'s your email')
        self.git_commands = ['add','am','apply','archive','bisect','blame','branch','bundle', 'checkout', 'cherry','cherry-pick','citool','clean','clone','commit','config','describe','diff','difftool','fetch','format-patch','fsck','gc','gitk','grep','gui','help','init','instaweb','log', 'ls-tree', 'merge','mergetool','mv','notes','push','range-diff','rebase','reflog','remote','repack','replace','request-pull','reset','revert','rm','send-email','shortlog','show','show-branch','stage','stash','status','submodule','tag','whatchanged','worktree',]
        self.git_opts = ["git", f"--git-dir={self.local}",  f"--work-tree={self.home}", "-c", f"user.name={self.cfg.username}", "-c", f"user.email={self.cfg.email}"]
        self.commands = ['ls']
        self.check_create_repo()
        if len(self.args) > 0 and self.args[0] in self.commands:
           self.__getattribute__(self.args[0])()
        elif len(self.args) > 0 and self.args[0] in self.git_commands:
            run(self.git_opts + self.args)
        else:
            run(self.git_opts + ['status', '-s'])

    def check_create_repo(self):
        if not os.path.exists(self.local):
            with open(os.path.join(self.home, '.gitignore'), 'w') as file:
                file.write(".cfg")
            clone = run(["git", "clone", "--bare", self.cfg.remote, self.local])
            if clone.returncode == 0:
                run(self.git_opts + ['config', '--local', 'status.showUntrackedFiles', 'no'])
                run(self.git_opts + ["master", "."])

    def ls(self):
        print('Files currently being tracked by dot:')
        run(self.git_opts + ["ls-tree", "master", "--name-only", "--full-tree", "-r"])

def main():
    Dot()

if __name__ == '__main__':
    main()

