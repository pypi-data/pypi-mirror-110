import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="gh_unwatch_except",
    version="0.0.1",
    author="Saimon Rai",
    description="A small utility for unwatching GitHub repositories.",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        'click',
        'PyGithub'
    ],
    py_modules=['gh_unwatch_except'],
    entry_points={
        'console_scripts': [
            'gh_unwatch_except = gh_unwatch_except:main',
        ],
    },
)
