import youtube_dl

ydl_opts = {'outtmpl':'%(title)s.%(ext)s'}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=IzAO9A9GjgI'])