# exec('from printr import printr')
from rich import print

# from needed_libs import *
# printr(['test'])
# sleep_for(hours=1)

# print = printr
# print(['test'])

libs_string = '''
# cc
import websocket, httpx
requests = httpx
from requests.exceptions import TooManyRedirects
from python_ghost_cursor import path
from price_parser import parse_price

# Mine
from timeout import sleep_timer, random_timeout, sleep_for
from printr import logger, print, current_time, same_line, printr
from error_alerts import telegram

# Socials
import tweepy, twitter, praw
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, FeedbackRequired, PleaseWaitFewMinutes, ClientThrottledError, ClientError
from telethon.sync import TelegramClient
from yt_dlp import YoutubeDL

# Scraping
import requestium, feedparser
from bs4 import BeautifulSoup
from selenium_shortcuts import setup_shortcuts

# Google
import gspread
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Server
from flask import Flask, render_template, request
from waitress import serve as server
from requests_futures.sessions import FuturesSession

# Misc
import schedule, demoji
from ffprobe import FFProbe
from dateutil.parser import parse as parse_date
'''

renamed_packages = [
    # Name to import, name to install via pip
    ['twitter', 'python-twitter'],
    ['timeout', 'python-timeout'],
    ['printr', 'python-printr'],
    ['dateutil', 'python-dateutil'],
    ['ffprobe', 'ffprobe-python'],
    ['yt_dlp', 'https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz']
    ]

libs = ['moviepy']
for line in libs_string.splitlines():
    for import_name, original_name in renamed_packages:
        line = line.replace(import_name, original_name)
    if line.startswith('import'):
        line = line.replace('import ', '')
        for lib in line.split(', '):
            if lib not in libs:
                libs.append(lib)
    elif line.startswith('from'):
        line = line.replace('from ', '')
        lib = line.split(' import ')[0]
        lib = line.split(' import ')[0]
        lib = lib.split('.')[0]
        if lib not in libs:
            libs.append(lib)

print(libs)