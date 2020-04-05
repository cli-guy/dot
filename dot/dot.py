#!/usr/bin/env python3
"""Usage:
  dot init [options...]
  dot <git_command> [git command options]
  dot remove
  dot -h | --help

Options:
  init
    --url GIT_URL        hosted git url
    --user GIT_USERNAME  git username to commit as
    --email GIT_EMAIL    git email to commit as
"""

__version__ = '1.0'

import os
import sys
import shutil
import datetime
from subprocess import run
from dot.config import Config

def checkout(cfg):
	response = run(cfg.base_cmd + cfg.args, capture_output=True)
	if response.returncode == 0:
		print("checkout complete")
	else:
		output = response.stderr.decode('utf-8').split("checkout:\n")[1].split("\nPlease move or")[0].replace('\t', "")
		print(f"The following files need to be moved \n\n{output}")
		if input('\nType yes to move them to .old_dotfiles or move then yourself and run checkout again: ') == 'yes':

			if not os.path.isdir(cfg.old_dotfiles):
				os.mkdir(cfg.old_dotfiles)
			for f in output.split('\n'):
				file_dir = os.path.split(f)[0]
				if len(file_dir) > 0 and os.path.isdir(os.path.join(cfg.old_dotfiles, file_dir)) == False:
					os.mkdir(os.path.join(cfg.old_dotfiles, os.path.split(f)[0]))
				shutil.move(os.path.join(cfg.home, f), os.path.join(cfg.old_dotfiles, f))
			checkout(cfg)

def display_help():
	sys.exit(__doc__)

def main():
	cfg = Config(__doc__)
	cfg.git_commands = ['add','am','apply','archive','bisect','blame','branch','bundle','cherry','cherry-pick','citool','clean','clone','commit','config','describe','diff','difftool','fetch','format-patch','fsck','gc','gitk','grep','gui','help','init','instaweb','log', 'ls-tree', 'merge','mergetool','mv','notes','pull','push','range-diff','rebase','reflog','remote','repack','replace','request-pull','reset','revert','rm','send-email','shortlog','show','show-branch','stage','stash','status','submodule','tag','whatchanged','worktree',]
	cfg.base_cmd = [
		"/usr/bin/git",
		f"--git-dir={os.path.join(cfg.home, '.cfg')}",
		f"--work-tree={cfg.home}",
	 	"-c", f"user.name={cfg.username}",
	 	"-c", f"user.email={cfg.email}"
	]
	cfg.old_dotfiles = os.path.join(cfg.home, ".old_dotfiles")
	if len(cfg.args) == 0:
		run(cfg.base_cmd + ["status"])

	elif cfg.args[0] == 'init':
		with open(os.path.join(cfg.home, '.gitignore'), 'w') as file:
			file.write(".cfg")
		clone = run(f"git clone --bare {cfg.repo} {os.path.join(cfg.home, '.cfg')} --verbose".split())
		if clone.returncode == 0:
			run(cfg.base_cmd + ['config', '--local', 'status.showUntrackedFiles', 'no'])

	elif cfg.args[0] == 'checkout':
		checkout(cfg)

	elif cfg.args[0] == 'ls':
		response = run(cfg.base_cmd + ["log", "--pretty=format:", "--name-only", "--diff-filter=A"], capture_output=True)
		ls = sorted(response.stdout.decode('utf-8').split('\n'))
		ls = list(filter(None, ls))
		print("\n".join(ls))

	elif cfg.args[0] == 'save':
		response = run(cfg.base_cmd + ["status"], capture_output=True)
		status = response.stdout.decode('utf-8').split('\n')
		if status[1].startswith("Changes"):
			status = [x.replace('\t', '') for x in status[5:-3]]
			print("\n".join(status))
			run(cfg.base_cmd + ["commit", "-a", "-m", str(datetime.datetime.now())])
			run(cfg.base_cmd + ["push", "origin", "master"])



	elif cfg.args[0] == 'remove':
		run(['rm', '-r', f'{cfg.home}/.gitignore', f'{cfg.home}/.cfg'])

	elif cfg.args[0] in cfg.git_commands:
		run(cfg.base_cmd + cfg.args)

	elif cfg.args[0] in ['-h', '--help']:
		display_help()

	else:
		display_help()

if __name__ == '__main__':
	main()
