from setuptools import setup

setup(
    name = 'tweetsole',
    version = '0.0.0',
    packages = ['tweetsole'],
    license = 'MIT',
    entry_points = {
        'console_scripts': [
            'tweetsole = tweetsole.__main__:main'
        ]
    },
    install_requires = [
            'simple-crypt',
            'tweepy',
            'pytest',
            'arrow'
            ]
    )
