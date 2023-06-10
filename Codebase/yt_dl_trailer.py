import yt_dlp as youtube_dl
import os
from conf import *
from plexapi.server import PlexServer 
import random
import time
from pathlib import Path
import re

#function to check if trailer is already present in the folder
def is_trailer_present(folder_path):
    for file in os.listdir(folder_path):
        file_name, file_ext = os.path.splitext(file)
        if file_name.endswith("-trailer"):
            return True
    return False

#function to search a <search_title> on youtube and download it to <folder path> and name it <filename>.ext
def download_movie_trailers(search_title, filename, folder_path, min_views=MIN_VIEWS, max_filesize_MB=MAX_FILESIZE_MB, min_filesize_MB=MIN_FILESIZE_MB):
    try:
        # Generate YouTube search query
        query = f"ytsearch:{search_title} trailer"
        max_filesize = max_filesize_MB * 1024 * 1024
        min_filesize = min_filesize_MB * 1024 * 1024

        output_filename = f"{filename} -trailer.%(ext)s"
        output_filepath = os.path.join(folder_path, output_filename)

        # Prepare options for downloading
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'outtmpl': output_filepath,
            'min_views':min_views,
            'max_filesize': max_filesize,
            'min_filesize': min_filesize,
            'quiet':True
        }

        # Download the trailers
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])

    except youtube_dl.DownloadError as e:
        print("Download Error:", e)


plex = PlexServer(PLEX_URL, TOKEN)
movies = plex.library.section(MOVIES_LIBRARY)

#iterate through all movies in Movies library
for movie in movies.all():

    #get attributes for the movie
    title = movie.title
    year = movie.year
    originalTitle = movie.originalTitle
    path = Path(movie.locations[0])
    folder_path = str(path.parent)

    #if trailer already exists, do nothing, and move to next movie
    if is_trailer_present(folder_path):
        print(f"Trailer already exists")

    else:
        #first prepare download filename
        #remove non-permissible characters from title
        print(f"\n\n{title} ({year}): ")
        title_validchars = re.sub('[/?%*|"<>:]+', "-", title)
        #if originalTitle exists, then remove non-permissible characters and enclose within brackets
        if originalTitle == None or originalTitle.strip() == '':
            originalTitle_validchars = ''
        else:
            originalTitle_validchars = " (" + re.sub('[/?%*|"<>:]+', "-", originalTitle) + ")"
        filename = f"{title_validchars} ({year}){originalTitle_validchars}"

        # try searching <title> on youtube for trailers, and download
        search_title = f"{title} ({year})"
        download_movie_trailers(search_title, filename, folder_path)
        if is_trailer_present(folder_path):
            print(f"Trailer found for {title}")
        else:
            # if <title> doesnt work, try <original title>
            print(f"Trailer not found for {title}")
            if originalTitle_validchars != '':
                search_title = f"{originalTitle} ({year})"
                download_movie_trailers(search_title, filename, folder_path) 
                if is_trailer_present(folder_path):
                    print(f"Trailer found for {originalTitle}")
                else:
                    print(f"Trailer not found for {originalTitle}")
        
        # sleep for a random duration. this is so that youtube doesnt get bombarded with requests
        # Youtube could introduce captcha if this is not done
        time.sleep(random.randint(1,MAX_SLEEP_DURATION))


