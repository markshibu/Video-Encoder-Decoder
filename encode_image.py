'''
encode_image.py - takes individual images, specified QF factor, and output file, and writes the encoded image to the output
Input - fimage, the image being encoded
		foutput, the output file being appended to
		QF - the quantization factor, used in encoding to suppress high frequencies
Output - none, encoding is written to file
Written by Jonathan Chamberlain - jdchambo@bu.edu
'''

import sys
import proto_mpeg
import cv2
import numpy as np

# parse inputs

fimage = sys.argv[1]
foutput = sys.argv[2]
QF = sys.argv[3]

# take image, convert to proto_mpeg Frame type
image = proto_mpeg.Frame(cv2.imread(fimage))

# open output file
f = open(foutput, "ab")

# starting from top left corner, take each MB and encode
for vert in range(0,image.v_mblocks):
	for hor in range(0,image.h_mblocks):
		MB = image.getBlock(vert, hor)
		encoded = image.encodeBlock(MB,QF)
		# write encoded to binary file
		
		
		

# close output file
f.close()