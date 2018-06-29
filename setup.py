from setuptools import setup

setup(
    name = 'tweeter',
    version = '0.0.0',
    packages = ['tweeter'],
    license = 'MIT',
    entry_points = {
        'console_scripts': [
            'tweeter = tweeter.__main__:main'
        ]
    },
    install_requires = [
            'simple-crypt',
            'tweepy',
            'pytest'
            ]
    )
