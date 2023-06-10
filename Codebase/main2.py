#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 00:16:32 2020

@author: konark
"""

from conf import *
import os
import sys
import re
from shutil import move
from pathlib import Path
from plexapi.server import PlexServer 


if LOG:
    log_file = open(codebase+"/log.txt",'w',encoding="utf-8")
else:
    log_file = sys.stdout


plex = PlexServer(PLEX_URL, TOKEN)
movies = plex.library.section(MOVIES_LIBRARY)
movies_path = movies.location[0]

for movie in movies.all():
    title = movie.title       
    year = movie.year
    originalTitle = movie.originalTitle
    location = movie.locations[0]
    
    location_path = Path(location)  
    current_folder_path = str(location_path.parent)
    
    current_movie_filename = location_path.stem
       
    title_validchars = re.sub('[/?%*|"<>:]+', "-", title)
    
    if originalTitle == None or originalTitle.strip() == '':
        originalTitle_validchars = ''
    else:
        originalTitle_validchars = " (" + re.sub('[/?%*|"<>:]+', "-", originalTitle) + ")"
    correct_movie_filename = f"{title_validchars} ({year}){originalTitle_validchars}"

    print(f"\n\nMovie : {correct_movie_filename}", file=log_file)
    print(f"Current Name : {current_movie_filename}", file=log_file)
    
    for file in os.scandir(current_folder_path):
        filePath = Path(file.path)
        filename = filePath.stem  
        if file.is_file():
            if filename.find(current_movie_filename) == 0:
                correct_filename = filename.replace(current_movie_filename,correct_movie_filename)
                correct_filepath = current_folder_path + "/" + correct_filename + filePath.suffix
                print(f"\nObject's filename is: {file.path}", file=log_file)
                print(f"Corrected filepath is: {correct_filepath}", file=log_file)
                try:
                    os.rename(file.path,correct_filepath)
                except PermissionError:
                    print('chflags nouchg "{}"'.format(file.path))
                    os.system('chflags nouchg "{}"'.format(file.path))
                    os.rename(file.path,correct_filepath)
                print("Rename completed", file=log_file)
                
  