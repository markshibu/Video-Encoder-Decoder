'''
encode.py - takes list of images as input, encodes them and saves as specified output file
Reuired Inputs - list of images (arbitrary number, assumed to be final inputs) 
optional inputs: output file (flagged with -output)
                 quantization factor (flagged with -qf, number between 0.1 and 1.5
Written by Jonathan Chamberlain - jdchambo@bu.edu
'''

import argparse
import sys
from os import listdir

def main():
	
	# get arguments, use argparse package to separate output, qf parameters and specify defaults
	
	parsed = argparse.ArgumentParser(description='Video encoder for jpeg images')
	parsed.add_argument('-output', nargs=1, default=['out.bin'], help='filename of encoded file - default is out.bin')
	parsed.add_argument('-qf', nargs=1, choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5], default=[0.8], help='quantization factor for high frquency supression. Default is 0.8')
	parsed.add_argument('input', nargs=argparse.REMAINDER, help='Specify either a space delimited list of files, or a single directory')
	
	args = parsed.parse_args()
	
	# If no arguments given, display help
	if (len(sys.argv[1:])) == 0:
		parsed.print_help()
		parsed.exit()
		
	# Get specified output file name
	fout = args.output[0]
	
	# Get input
	if args.input == []:
		print("No input files detected... aborting. Use -h to view help.")
		parsed.exit()
	else:
		# determine if input[0] is directory. If not, assume it is a list of filenames
		try:
			directory = sorted(listdir(args.input[0]))
			# append trailing forward slash if not present, otherwise will cause error with fetching the file names
			if args.input[0][-1] != '/':
				args.input[0] = args.input[0] + '/'
			fin = [args.input[0]+fname for fname in directory]
			# directory specified, but multiple inputs detected
			if len(args.input) > 1:
				print("Additional input parameters ignored following directory. Use -h to view help.")
		# not a dreictory, assume filenames
		except NotADirectoryError:
			fin = args.input
	
	# call video encoder
	
if __name__ == "__main__":
	main()
