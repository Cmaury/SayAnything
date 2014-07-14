import os
from pydub import AudioSegment

#Global Vars
workingDirectory = '.'
targetDirectory = './snippets'

#Get files
def sliceFiles(dir = workingDirectory, targetDirectory = targetDirectory):
	workingDirectory = dir
	files = files = os.listdir(dir)
	for file in files:
		sliceSong(file)

#slice song into minute long snippets
def sliceSong(filename):
	song = AudioSegment.from_wav(workingDirectory + filename)
	#detectPauses()
	length = song.duration_minutes
	for i in range(0,length - 1):
		saveSongSnippets(song[i:i+1], str(i))


def saveSongSnippets(snippet, targetFileName):
		snippet.export(targetDirectory + "/" + targetFileName + ".wav", format="wav")	