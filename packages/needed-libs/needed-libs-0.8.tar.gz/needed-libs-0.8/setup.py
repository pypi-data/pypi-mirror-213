from setuptools import setup

# from needed_libs import imports_string
# renamed_packages = [
#     ['twitter', 'python-twitter'],
#     ['timeout', 'python-timeout'],
#     ['printr', 'python-printr'],
#     ]

# libs = ['moviepy']
# for line in imports_string.splitlines():
#     for import_name, original_name in renamed_packages:
#         line = line.replace(import_name, original_name)
#     if line.startswith('import'):
#         line = line.replace('import ', '')
#         for lib in line.split(', '):
#             if lib not in libs:
#                 libs.append(lib)
#     elif line.startswith('from'):
#         line = line.replace('from ', '')
#         lib = line.split(' import ')[0]
#         lib = lib.split('.')[0]
#         if lib not in libs:
#             libs.append(lib)
# print(libs)

setup(
    name = 'needed-libs',
    packages = ['needed_libs'],
    version = '0.8',
    install_requires = [
        # cc
        'websocket',
        'httpx',
        'requests',
        'python_ghost_cursor',
        'price_parser',
        
        # Mine
        'python-timeout',
        'python-printr',
        'error_alerts',
        
        # Socials     
        'tweepy',
        'python-twitter',     
        'praw',
        'instagrapi',
        'moviepy',
        'telethon',
        'yt-dlp',
        
        # Scraping
        'requestium',
        'feedparser',
        'bs4',
        'selenium_shortcuts',

        # Google
        'gspread',
        'googleapiclient',
        'google_auth_oauthlib',
        'google',

        # Server
        'flask',
        'waitress',
        'requests_futures',
        
        # Misc
        'schedule',
        'demoji',
        'ffprobe-python',
        'python-dateutil',
        ]
    )