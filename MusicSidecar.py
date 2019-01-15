import os, json, errno
from tinytag import TinyTag
from argparse import ArgumentParser

#grab arguments
parser = ArgumentParser()
parser.add_argument('rootDirectory', help='root directory which music-sidecar should start work', metavar='rootDirectory', nargs='+')
parser.add_argument('-onePerDirectory', help='only create one sidecar file per directory', action='store_true')
parser.add_argument('-clean', help='remove all previously generated sidecar files', action='store_true')
args = parser.parse_args()

supportedFileTypes = ['.mp3', '.flac']

#process audio files into sidecars
def main():
    for rootdirectory in args.rootDirectory:
        print('%s: looking for audio in sub-directories' % rootdirectory)
        directories = get_audio_directories(rootdirectory)

        for directory in directories:
            print('%s: working on audio files' % directory)
            
            #clean up any existing sidecar files
            if(args.clean):
                for filename in (file for file in os.listdir(directory) if file.endswith('.json')):
                    silentremove(directory + '/' + filename)
                continue

            #create one sidecar per directory
            if(args.onePerDirectory):
                silentremove(directory + '/' + 'sidecar.json')
                files = []

                for filename in (file for file in os.listdir(directory) if os.path.splitext(file)[-1].lower() in supportedFileTypes):
                    files.append(get_meta_data(directory, filename))

                with open(directory + '/sidecar.json', 'w') as fp:
                        json.dump(files, fp)

            #create one sidecar per file
            if(args.onePerDirectory == False):
                for filename in (file for file in os.listdir(directory) if os.path.splitext(file)[-1].lower() in supportedFileTypes):
                    metaData = json.dumps(get_meta_data(directory, filename), indent=2)
                    with open(directory + '/' + filename + '-sidecar.json', 'w') as fp:
                        json.dump(metaData, fp)

            print('%s: finished work in directory' % directory)
    print('%s: finished work in all sub directories' % rootdirectory)

#return a list of all directories that contains audio files,
def get_audio_directories(path):
    directorylist = []

    #return nothing if path is a file
    if os.path.isfile(path):
        return []

    #add dir to directorylist if it contains on of the supported file types
    if any(os.path.splitext(file)[-1].lower() in supportedFileTypes for file in os.listdir(path)):
        directorylist.append(path)

    for d in os.listdir(path):
        new_path = os.path.join(path, d)
        if os.path.isdir(new_path):
            directorylist += get_audio_directories(new_path)

    return directorylist
    
#returns the tags from the supplied audio file
def get_meta_data(path, filename):
    tags = TinyTag.get(path + '/' + filename)
    return {'filename':filename,
            'album':tags.album,
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

#delete the supplied file if it exists
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: 
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

main()






