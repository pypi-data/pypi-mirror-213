from setuptools import setup

setup(
    name = 'needed-libs',
    packages = ['needed_libs'],
    version = '0.6',
    install_requires = [
        # cc
        'websocket-client',
        'python_ghost_cursor',
        'price_parser',
        'requests',

        # Mine
        'python-timeout',
        'python-printr',
        'error-alerts',

        # Socials
        'tweepy',
        'python-twitter',
        'instagrapi',
        'moviepy',
        'telethon',

        # Scraping
        'bs4',
        'httpx',
        'selenium-shortcuts',
        'undetected-chromedriver',
        'requestium',
        'feedparser',

        # Google
        'gspread',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',

        # Server
        'flask',
        'waitress',
        
        # Misc
        'python-dateutil',
        'demoji',
        'schedule',
        'ffprobe-python',
        ]
    )