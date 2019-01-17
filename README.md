# music-sidecar

Python application to generate sidecar files from audio files. Sidecar files contain a copy of the ID3 information and the filename. Either create a sidecar for each audio file, or a single "sidecar" file for the directory containing the audio files.

Installation:

```bash
#install pipenv if required
pip install --user pipenv

#clone this repo and cd to the directory
pipenv install
pipenv run pythong MusicSidecar.py [arguments - see usage below]
```

Usage:

```bash
#generate a sidecar file per audio file
pipenv run python MusicSidecar.py /root/directory/path

#generate a sidecar file per directory
pipenv run python MusicSidecar.py /root/directory/path -onePerDirectory

#clear all existing sidecar files
pipenv run python MusicSidecar.py /root/directory/path -clean
```

