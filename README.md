# music-sidecar

Python application to generate sidecar files from audio files, containing a copy of the ID3 information and filename. Either create a sidecar for each audio file, or a single "sidecar" file for the directory containing the audio files.

Usage:

```bash
#generate a sidecar file per audio file
pipenv run python MusicSidecar.py /root/directory/path

#generate a sidecar file per directory
pipenv run python MusicSidecar.py /root/directory/path -onePerDirectory

#clear all existing sidecar files
pipenv run python MusicSidecar.py /root/directory/path -clean
```

