#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 00:16:32 2020

@author: konark
"""
test = 1
test_case = 4
log = 1

from conf import *
import os
import sys
import re
from shutil import move
from pathlib import Path
from plexapi.server import PlexServer 

if test == 1:
    movies_path = codebase + "/Test_" + str(test_case)
elif test == 0:
    movies_path = plex_movies_path
else:
    print('Test field not set properly')
    raise

if log == 1:
    log_file = open(codebase+"/log.txt",'w',encoding="utf-8")
else:
    log_file = sys.stdout


plex = PlexServer(plex_url, token)
movies = plex.library.section('Movies')

for video in movies.search():
    title = video.title       
    year = video.year
    originalTitle = video.originalTitle
    location = video.locations[0]
    
    location_path = Path(location.replace(plex_movies_path, movies_path))
    
    current_folder_path = str(location_path.parent)
    
    current_movie_filename = location_path.stem
       
    title_validchars = re.sub('[/?%*|"<>:]+', "-", title)
    
    if originalTitle == None or originalTitle.strip() == '':
        originalTitle_validchars = ''
    else:
        originalTitle_validchars = "(" + re.sub('[/?%*|"<>:]+', "-", originalTitle) + ") "
    correct_movie_filename = "{0} ({1}) ({2})".format(title_validchars, year, originalTitle_validchars)

    print("\n\nMovie : ",correct_movie_filename, file=log_file)
    print("Current Name :",current_movie_filename, file=log_file)
    
    for file in os.scandir(current_folder_path):
        filePath = Path(file.path)
        filename = filePath.stem  
        if file.is_file():
            if filename.find(current_movie_filename) == 0:
                correct_filename = filename.replace(current_movie_filename,correct_movie_filename)
                correct_filepath = current_folder_path + "/" + correct_filename + filePath.suffix
                print("\nObject's filename is: {0}".format(file.path), file=log_file)
                print("Corrected filepath is: {0}".format(correct_filepath), file=log_file)
                os.rename(file.path,correct_filepath)
                print("Rename completed", file=log_file)
                
  