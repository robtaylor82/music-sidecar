import os, json
from tinytag import TinyTag
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('rootDirectories', help='The root directory which MusicSidecar should start work.', metavar='DIR', nargs='+')
args = parser.parse_args()

supportedFileTypes = ['.mp3', '.flac']

#returns a list of all directories that contains audio files,
def getAudioDirectories(path):
    directoryList = []

    #return nothing if path is a file
    if os.path.isfile(path):
        return []

    #add dir to directorylist if it contains on of the supported file types
    if any(os.path.splitext(file)[-1].lower() in supportedFileTypes for file in os.listdir(path)):
        directoryList.append(path)

    for d in os.listdir(path):
        new_path = os.path.join(path, d)
        if os.path.isdir(new_path):
            directoryList += getAudioDirectories(new_path)

    return directoryList
    
#returns the tags from the audio file
def getMetaData(audioFile):
    tags = TinyTag.get(audioFile)
    return {'album':tags.album,
            'albumartist':tags.albumartist,
            'artist':tags.artist,
            'disk':tags.disc,
            'disktotal':tags.disc_total,
            'duration':tags.duration,
            'genre':tags.genre,
            'title':tags.title,
            'track':tags.track,
            'year':tags.year
            } 



for rootDirectory in args.rootDirectories:
    print('looking for audio in sub-directories under %s' % rootDirectory)
    audioDirectories = getAudioDirectories(rootDirectory)
    for audioDirectory in audioDirectories:
        print('working on audio files in directory: %s' % audioDirectory)
        for musicFile in (file for file in os.listdir(audioDirectory) if os.path.splitext(file)[-1].lower() in supportedFileTypes):
            fileName = audioDirectory + '/' + musicFile
            metaData = json.dumps(getMetaData(fileName), indent=2)
            with open(fileName + '-sidecar.json', 'w') as fp:
                json.dump(metaData, fp)







