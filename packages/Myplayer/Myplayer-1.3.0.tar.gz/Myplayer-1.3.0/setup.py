from setuptools import setup

setup(
    name='Myplayer',
    version='1.3.0',
    author='Eduardo Martins Panassi',
    author_email='edumartinpanassi@gmail.com',
    description='Um reprodutor de músicas em python!',
    packages=['myplayer'],
    install_requires=[
        'pygame',
    ],
)
