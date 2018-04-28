'''
view.py - takes binary file input stream, and uses this to generate video playback
Input - compressed binary file
Written by Jonathan Chamberlain - jdchambo@bu.edu
'''

import sys
import proto_mpeg
import cv2

# get and open file name
fin = sys.argv[1]
f = open(fin, "rb")

# parse file, get images
# fill in code later, store images in Stream

# playback 
for image in Stream:
	# determine how to display images in stream

