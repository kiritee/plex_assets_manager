#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file
"""
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv)

PLEX_API_TOKEN  = os.getenv('PLEX_API_TOKEN')

LOG = True
QUIET = False


PLEX_URL = "http://127.0.0.1:32400"

MOVIES_LIBRARY = 'Movies'

#youtube trailer download conf
MIN_VIEWS=10000
MAX_FILESIZE_MB=100
MIN_FILESIZE_MB=1
MAX_SLEEP_DURATION=15

