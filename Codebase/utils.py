import yt_dlp as youtube_dl
from conf import MIN_VIEWS, MAX_FILESIZE_MB, MIN_FILESIZE_MB
import os

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
