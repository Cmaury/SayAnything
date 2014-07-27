import os
from pydub import AudioSegment

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
	print('working directory ' + dir)
	files = files = os.listdir(dir)
	print(files)
	for file in files:
		if file.endswith('.WAV'):
			print('slicing file ' + file)
			sliceSong(file)

#slice song into minute long snippets
def sliceSong(filename):
	song = AudioSegment.from_wav(workingDirectory + filename)
	print('creating song object for ' + filename)
	#detectPauses()
	length = int(song.duration_seconds / 60)
	one_minute = 60*1000
	print('length is ' + str(length))
	global filecounter
	for i in range(0,length):
		saveSongSnippets(song[i * one_minute:i * one_minute + one_minute], str(filecounter))
		print('saving song snippet...' + str(filecounter))
		filecounter += 1


def saveSongSnippets(snippet, targetFileName):
		snippet.export(targetDirectory + targetFileName + ".wav", format="wav")
		print('song snippet ' + targetFileName + ' saved')	



		sliceFiles('/Users/cmaury/CLabs/AudioResearch/RawRecordings/07-10-14','/Users/cmaury/CLabs/AudioResearch/snippets/7-10-14')
		sliceSong('/Users/cmaury/CLabs/AudioResearch/RawRecordings/07-10-14/ZOOM0001.WAV')
