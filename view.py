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
		print("No binary file specified as first argument... aborting. Use -h to view help.")
		parsed.exit()
	
	# if multiple inputs detected, ignore
	if len(args.input) > 1:
		print("Additional input arugments detected... ignoring. Use -h to view help.")
	
	# Pass to decoder/viewer:
	decode_video(18,32,fin,0.8)
	

if __name__ == "__main__":
	main()
