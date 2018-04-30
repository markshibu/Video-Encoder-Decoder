'''
view.py - takes binary file input stream, and uses this to generate video playback
Input - compressed binary file
Written by Jonathan Chamberlain - jdchambo@bu.edu
Some argument parsing code adapted from https://github.com/appletonbrian/EC504-video-encoder
'''

import sys
import argparse
from decoder import decode_video

def main():

	# get file input
	parsed = argparse.ArgumentParser(description='Decoder and viewer for compressed binary video files')
	parsed.add_argument('--fps', nargs=1, choices=['5','10','15','20'], default=['10'], help = 'Specify frames per second of video. Default is 10')
	parsed.add_argument('--output',nargs=1, default='decoded_movie.mp4', help='Specify mp4 filename for video. Default is decoded_movie.mp4')
	parsed.add_argument('input', nargs=argparse.REMAINDER, help='Specify a binary file containing a compressed video file')

	# get args
	args = parsed.parse_args()

	# No arguments given, display help
	# If no arguments given, display help
	if (len(sys.argv[1:])) == 0:
		parsed.print_help()
		parsed.exit()

	# check that is a binary file
	fin = args.input[0]
	if not fin.lower().endswith('.bin'):
		print("No binary file specified as input argument... aborting. Use -h to view help.")
		parsed.exit()
	
	# if multiple inputs detected, ignore
	if len(args.input) > 1:
		print("Additional input arugments detected... ignoring. Use -h to view help.")
	
	# get fps
	FPS = int(args.fps[0])
	
	# get output file name
	fout = args.output[0]
	
	#if mp4 filename not sepcified, append mp4 extension
	if not fout.lower().endswith(".mp4"):
		fout = fout + ".mp4"
	
	# Pass to decoder/viewer:
	decode_video(fin,FPS,fout)
	

if __name__ == "__main__":
	main()
