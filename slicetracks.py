import logging
import os
from pydub import AudioSegment

logging.basicConfig(filename='logs.log',level=logging.DEBUG)

#Global Vars
workingDirectory = './'
targetDirectory = './snippets/'
filecounter = 0

#Get files
def sliceFiles(dir = workingDirectory, targetDir= targetDirectory):
    global workingDirectory
    workingDirectory = dir + '/'
    global targetDirectory
    targetDirectory =  targetDir + '/'
    logging.debug('working directory ' + dir)
    files = files = os.listdir(dir)
    logging.debug(files)
    for file in files:
        if file.endswith('.WAV'):
            logging.info('slicing file ' + file)
            sliceSong(file)

#slice song into minute long snippets
def sliceSong(filename):
    song = AudioSegment.from_wav(workingDirectory + filename)
    logging.debug('creating song object for ' + filename)
    #detectPauses()
    length = int(song.duration_seconds / 60)
    one_minute = 60*1000
    logging.debug('length is ' + str(length))
    global filecounter
    for i in range(0,length):
        saveSongSnippets(song[i * one_minute:i * one_minute + one_minute], str(filecounter))
        logging.debug('saving song snippet...' + str(filecounter))
        filecounter += 1

def saveSongSnippets(snippet, targetFileName):
        snippet.export(targetDirectory + targetFileName + ".wav", format="wav")
        logging.info('song snippet ' + targetFileName + ' saved')    

