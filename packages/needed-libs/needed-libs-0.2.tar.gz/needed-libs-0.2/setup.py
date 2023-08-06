from setuptools import setup

setup(
    name = 'needed-libs',
    packages = ['needed-libs'],
    version = '0.2',
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
        'selenium-shortcurts',
        'undetected-chromedriver',
        'requestium',
        'feedparser',

        # Google
        'gspread',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        
        # Misc
        'flask',
        'waitress',
        'python-dateutil',
        'demoji',
        'schedule',
        'ffprobe-python',
        ]
    )