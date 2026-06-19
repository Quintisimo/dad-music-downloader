# Dead As Disco Music Downloader

A simple wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [bpm-tools](https://www.pogo.org.uk/~mark/bpm-tools/) to search, download songs from YouTube and add it to the game [Dead As Disco](https://deadasdisco.com/).

## IMPORT_SONGS_PATH

This changes based on the os you are using:

- Windows: `%localappdata%/Pagoda/Saved/ImportedSongs`
- Linux: run `find ~/.local/share/Steam/steamapps/compatdata -type d -name ImportedSongs` to find the path

Run the cli:

The game should not be running when you run the CLI.

```bash
  docker run --privileged --rm -it -v "IMPORT_SONGS_PATH:/app/songs" ghcr.io/quintisimo/dad-music-downloader:latest
```

OR

```bash
  podman run --privileged --rm -it -v "IMPORT_SONGS_PATH:/app/songs" ghcr.io/quintisimo/dad-music-downloader:latest
```
