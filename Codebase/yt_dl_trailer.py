import yt_dlp as youtube_dl
import os
from conf import *
from plexapi.server import PlexServer 
import random
import time
from pathlib import Path
import re

def is_trailer_present(folder_path):
    for file in os.listdir(folder_path):
        file_name, file_ext = os.path.splitext(file)
        if file_name.endswith("-trailer"):
            return True
    return False

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


plex = PlexServer(plex_url, token)
movies = plex.library.section('Movies')

for movie in movies.all():
    title = movie.title
    year = movie.year
    originalTitle = movie.originalTitle
    path = Path(movie.locations[0])
    folder_path = str(path.parent)

    print(f"\n\n{title} ({year}): ")
    title_validchars = re.sub('[/?%*|"<>:]+', "-", title)
    if originalTitle == None or originalTitle.strip() == '':
        originalTitle_validchars = ''
    else:
        originalTitle_validchars = " (" + re.sub('[/?%*|"<>:]+', "-", originalTitle) + ")"
    filename = "{0} ({1}){2}".format(title_validchars, year, originalTitle_validchars)

    if is_trailer_present(folder_path):
        print(f"Trailer already exists")

    else:
        search_title = f"{title} ({year})"
        download_movie_trailers(search_title, filename, folder_path)
        if is_trailer_present(folder_path):
            print(f"Trailer found for {title}")
        else:
            print(f"Trailer not found for {title}")
            if originalTitle_validchars != '':
                search_title = f"{originalTitle} ({year})"
                download_movie_trailers(search_title, filename, folder_path) 
                if is_trailer_present(folder_path):
                    print(f"Trailer found for {originalTitle}")
                else:
                    print(f"Trailer not found for {originalTitle}")

        time.sleep(random.randint(1,MAX_SLEEP_DURATION))


