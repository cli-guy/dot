from setuptools import setup, find_packages

setup(
    name='jp-dot',
    version='1.0',
    description='dot, a git bare repository wrapper for managing dotfiles.',
    author='James Phillips',
    license='GPLv3',
    packages=find_packages(),
    author_email='james@mightysteedit.co.uk',
    install_requires=["jp-config"],
    url="https://github.com/cli-guy/dot",
    entry_points = {
        'console_scripts' : ['dot = jpdot.jpdot:main']
    }
    )
