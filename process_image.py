'''
Process_image.py - takes as input 16x16x3 matrix, corresponding to a Macroblock of the image
Outputs the result of the DCT transformation and Quantization
Inputs - M, the Macroblock
	 Q, the image compression quality, used in quanitzation
Output - B, collection of blocks followign transformation/quantization
Written by Jonathan Chamberlain - jdchambo@bu.edu
'''

import numpy
import sys

'''
Definitions for 2D DCT
Functions origionally written by Mark Newman <mejn@umich.edu>
Accessed from http://www-personal.umich.edu/~mejn/computational-physics/dcst.py
Source contains blurb : "You may use, share, or modify this file freely"
'''
from numpy import empty,arange,exp,real,imag,pi
from numpy.fft import rfft,irfft


def dct(y):
    N = len(y)
    y2 = empty(2*N,float)
    y2[:N] = y[:]
    y2[N:] = y[::-1]

    c = rfft(y2)
    phi = exp(-1j*pi*arange(N)/(2*N))
    return real(phi*c[:N])

# 2D DCT

def dct2(y):
    M = y.shape[0]
    N = y.shape[1]
    a = empty([M,N],float)
    b = empty([M,N],float)

    for i in range(M):
        a[i,:] = dct(y[i,:])
    for j in range(N):
        b[:,j] = dct(a[:,j])

    return b

'''
Beginning of functions written for process_image
'''

M = sys.argv[1]
Q = sys.argv[2]

# define individual blocks B1, B2, B3, B4, S.t. M is subdivided as
# B1 | B2
# _  _ _
# B3 | B4

# These blocks will contain the Y' component of the coloration of the pixel
B1 = numpy.zeros(shape=(8,8))
B2 = numpy.zeros(shape=(8,8))
B3 = numpy.zeros(shape=(8,8))
B4 = numpy.zeros(shape=(8,8))

# We subsample the Rb, Rr components to compress data - take data from B1 block only 
Bb = numpy.zeros(shape=(8,8))
Br = numpy.zeros(shape=(8,8))
# populate B1, B2, B3, B4, Bb, Br with image data
# data in M stored as RGB, convert to Y'RbRr - use JPEG standard


for i in range(0,8):
	for j in range(0,8):
		B1[i,j] = (0.299*M.red[i,j])+(0.587*M.green[i,j])+(0.114*M.blue[i,j])
		B2[i,j] = (0.299*M.red[i,j+8])+(0.587*M.green[i,j+8])+(0.114*M.blue[i,j+8])
		B3[i,j] = (0.299*M.red[i+8,j])+(0.587*M.green[i+8,j])+(0.114*M.blue[i+8,j])
		B4[i,j] = (0.299*M.red[i+8,j+8])+(0.587*M.green[i+8,j+8])+(0.114*M.blue[i+8,j+8])
		Bb[i,j] = 128 - (0.168736*M.red[i,j]) - (0.331264*M.green[i,j]) + (0.5*M.blue[i,j])
		Br[i,j] = 128 + (0.5*M.red[i,j]) - (0.418688*M.green[i,j])- (0.081312*M.blue[i,j])

# for each matrix layer, run 2D DCT
# subsample layers 2,3 by only running 2D DCT on these layers for B1

# for now, Y cooresponds to R layer, Rb to B layer, Rr to G layer
print B1
B1 = dct2(B1) 
B2 = dct2(B2) 
B3 = dct2(B3) 
B4 = dct2(B4) 
Bb = dct2(Bb) 
Br = dct2(Br) 

print B1
'''
Quantization steps for each matrix
'''

#define base quantization matrix - taken from IJG standard 
Qb = numpy.matrix('16 11 10 16 24 40 51 61;12 12 14 19 26 58 60 55;14 13 16 24 40 57 69 56;14 17 22 29 51 87 80 62;18 22 37 56 68 109 103 77;24 35 55 64 81 104 113 92;49 64 78 87 103 121 120 101;72 92 95 98 112 100 103 99') 

# from quaity factor, determine multiplication factor for quantization
if Q < 50:
	S = 5000/Q;
else:
	S = 200 - 2*Q;
	


# determine quantized matrix result
for i in range (0,8):
	for j in range (0,8):
		Qf = (S*Qb[i,j] + 50) // 100
		if Qf == 0:
			Qf = 1
		B1[i,j] = B1[i,j] // Qf
		B2[i,j] = B2[i,j] // Qf
		B3[i,j] = B3[i,j] // Qf
		B4[i,j] = B4[i,j] // Qf
		Bb[i,j] = Bb[i,j] // Qf
		Br[i,j] = Br[i,j] // Qf
		
# define the collection of the 6 processed blocks, and return
B = [B1, B2, B3, B4, Bb, Br]
print B1
