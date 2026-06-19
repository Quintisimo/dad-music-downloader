import subprocess
import random
import json

import cutie
import yt_dlp
from youtube_search import YoutubeSearch

try:
    search = input("Search for a song: ")
    results = YoutubeSearch(search, max_results=10).to_dict()

    titles = [
        f"{result['title']} [{result['channel']}] [{result['duration']}] [{result['views']}]"
        for result in results
    ]
    video = results[cutie.select(titles)]
    name = video["title"]
    url = f"https://www.youtube.com/watch?v={video['id']}"
except KeyboardInterrupt:
    exit(0)


# https://www.xmodhub.com/info/xmod-blog/dead-as-disco-custom-music/
sample_rate = "44100"
format = "ogg"
folder = f"songs/{name}"
song_path = f"{folder}/Audio"

ydl_opts = {
    "format": f"{format}/bestaudio/best",
    "outtmpl": song_path,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "vorbis",
            "preferredquality": "192",  # bitrate in kbps (optional)
        }
    ],
    "postprocessor_args": {
        "extractaudio": ["-ar", sample_rate],  # sample rate → ffmpeg
    },
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download([url])
    if error_code:
        print(f"Download failed with error code: {error_code}")
        exit(1)

    bpm = subprocess.check_output(
        # https://gist.github.com/brimston3/34dbb439442a723313b019b92931887b
        f'ffmpeg -vn -i "{song_path}.{format}" -ar {sample_rate} -ac 1 -f f32le pipe:1 2>/dev/null | bpm',
        shell=True,
        text=True,
    ).strip()

    meta = {
      "version": 1,
      "uniqueId": random.randint(100000000, 999999999),
      "songName": name,
      "performedBy": [video["channel"]],
      "writtenBy": [video["channel"]],
      "seed": random.randint(100000000, 999999999),
      "tempo": int(float(bpm)),
      "customTempoSections": [],
      "beatOffset": 0,
      "startSongOffset": 0,
      "endSongOffset": 0,
      "uEAssetName": name,
      "originalAudioFileHash": "",
      "originalAudioFilePath": ""
    }

    with open(f"{folder}/Meta.json", "w") as f:
        json.dump(meta, f, indent=2)
