'''
encode_image.py - takes individual images, specified QF factor, and output file, and writes the encoded image to the output
Input - image, the image being encoded
		output, the output file being appended to
		QF - the quantization factor, used in encoding to suppress high frequencies
Output - none, encoding is written to file
Written by Jonathan Chamberlain - jdchambo@bu.edu
'''

import sys
import proto_mpeg

# parse inputs

image = sys.argv[1]
output = sys.argv[2]
QF = sys.argv[3]

# 