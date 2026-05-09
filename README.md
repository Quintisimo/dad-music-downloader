# Dead As Disco Music Downloader

A simple wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [bpm-tools](https://www.pogo.org.uk/~mark/bpm-tools/) to download songs from YouTube and analyze their BPM to add to the game [Dead As Disco](https://deadasdisco.com/).

Run the cli:

```bash
  docker run --rm -it -v "$PWD/songs:/app/songs" ghcr.io/quintisimo/dad-music-downloader:latest
```
