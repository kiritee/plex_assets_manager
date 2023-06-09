#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:24:49 2020

@author: konark
"""


token='3SUVxp5_DJw2nqt4snLW'
plex_url="127.0.0.1:32400"
from plexapi.server import PlexServer 
plex = PlexServer(plex_url, token)
movies = plex.library.section('Movies')
for video in movies.search():
    print(video.title+' ('+str(video.year)+')', )