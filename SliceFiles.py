#!/usr/bin/env python
# Description: This module is responsible for the slicing, or splitting, of audio files into more manageable chunks

# standard imports
import argparse
import logging
import os
import ntpath

# external imports
from pydub import AudioSegment

def main():
 """Main function to kick things off"""
 args = parseArgs()
 # setup the loger
 logging.basicConfig(filename=args.logfile, level=getattr(logging, args.log_level.upper(), None), filemode='w')

 if args.batch:
  sliceFiles(args.input, args.output, args.pretend)
 else:
  sliceFile(args.input, args.output, args.pretend)

def parseArgs():
 """Setup and run the commandline argument parser """
 parser = argparse.ArgumentParser(
 description = "This script performs the following actions\n \
 1. Itterates through input directory or single file, splitting input files into one minute snippets.\n",
 formatter_class = argparse.RawTextHelpFormatter
 )
 parser.add_argument('-b', '--batch', help='Runs the script in batch mode', action='count')
 parser.add_argument('-l', '--log-level', help='Set the debug level for the logger', choices=['debug', 'info', 'warning', 'error', 'critical'], default='debug')
 parser.add_argument('-i', '--input', help='Input path for file or directory', required=True)
 parser.add_argument('-f', '--logfile', help='Path for log file', default='logs.log')
 parser.add_argument('-o', '--output', help='Output path for file or directory', default='./snippets')
 parser.add_argument('-p', '--pretend', help='Runs the script in pretend mode, not actually changing any files', action='count')
 return parser.parse_args()

def extractFilenameFromPath(path):
 """Returns the filename portion of a path on all platforms, but does assume no Linux files with backslashes in their names."""
 head, tail = ntpath.split(path)
 tail = tail or ntpath.basename(head)
 logging.debug('extractFilename: head='+head+' tail='+tail)
 return tail or ntpath.basename(head)

def sliceFile(filePath, targetDir, pretend=False):
 """Splits an audio file into one minute chunks.

 Input:
 filePath: An audio file's fully qualified filename as a string
 targetDir: The directory in which to save one minute chunks.
 pretend: A boolean controlling whether writes are actually performed

 Output:
 Saves one minute chunks of file in provided dir

 Returns:
 The number of chunks created e.g. this should be equal to the duration of the file, in seconds, divided by 60, [plus 1 if file is not an exact number of minutes long]
 """
 logging.debug('creating AudioSegment object for ' + filePath)
 file = AudioSegment.from_wav(filePath)
 lengthInSeconds = file.duration_seconds
 logging.debug('File is %d seconds long.'%(lengthInSeconds))

 if not os.path.exists(targetDir):
  os.makedirs(targetDir)
 slicePrefix = filePath
 if filePath.count('/') > 0 or filePath.count('\\') > 0:
  slicePrefix = extractFilenameFromPath(filePath)

 # chop 3 letter extension off name in prefix
  slicePrefix = slicePrefix[:-4]


 # itterate through the file one minute at a time, saving off slice into targetDir
 for i in range(0, int(lengthInSeconds*1000), 60000):
  slicePath = targetDir+'/'+slicePrefix+str(i/1000)+'.wav'
  logging.debug('Writing slice: '+slicePath)
  if not pretend:
   file[i:i+60000].export(slicePath, format='wav')

def sliceFiles(sourceDir, targetDir, pretend=False):
 """Itterates across sourceDir, looking for .wav files, and then passes them to sliceFile function

 input:
 sourceDir: a fully qualified path to a source directory
 targetDir: A fully qualified path to a target directory to put the slices
 pretend: A boolean controlling whether writes are actually performed
 """

 logging.info('Scanning '+sourceDir+' for wave files to slice.')
 files = os.listdir(sourceDir)
 logging.debug(files)
 for file in files:
  if file.lower().endswith('.wav'):
   logging.info('slicing file ' + file)
   sliceFile(sourceDir+'/'+file, targetDir, pretend)

if __name__ == "__main__":
 main()
