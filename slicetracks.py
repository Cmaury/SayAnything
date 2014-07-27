#!/usr/bin/python

import argparse
import logging
import os
from pydub import AudioSegment

parser = argparse.ArgumentParser(
description = "This script performs the following actions\n \
1. Itterates through input directory or single file, splitting input files into one minute snippets.\n",
formatter_class = argparse.RawTextHelpFormatter
)
parser.add_argument('-b', '--batch', help='Runs the script in batch mode', action='count')
parser.add_argument('-l', '--log-level', help='Set the debug level for the logger', choices=['debug', 'info', 'warning', 'error', 'critical'], default='info')
parser.add_argument('-i', '--input', help='Input path for file or directory', required=True)
parser.add_argument('-f', '--logfile', help='Path for log file', default='logs.log')
parser.add_argument('-o', '--output', help='Output path for file or directory', required=True)
parser.add_argument('-p', '--pretend', help='Runs the script in pretend mode, not actually changing any files', action='count')
args = parser.parse_args()

logging.basicConfig(filename=args.logfile, level=getattr(logging, args.log_level.upper(), None))

#Global Vars
workingDirectory = './'
targetDirectory = './snippets/'
filecounter = 0

#Get files
def sliceFiles(dir, targetDir):
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
    if not args.pretend:
        snippet.export(targetDirectory + targetFileName + ".wav", format="wav")
    logging.info('song snippet ' + targetFileName + ' saved')    

sliceFiles(args.input, args.output)
