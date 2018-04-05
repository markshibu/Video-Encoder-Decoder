'''
Process_image.py - takes as input 16x16x3 matrix, corresponding to a Macroblock of the image
Outputs the result of the DCT transformation and Quantization
Inputs - M, the Macroblock
		 Q, the image compression quality, used in quanitzation
Output - O, the Macroblock following transformation and Quantization
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
Image processing begins
'''

# M = sys.argv[1]
# Q = sys.argv[2]

M = numpy.ones(shape=(16,16,3))
Q = 100

# define individual blocks B1, B2, B3, B4, S.t. M is subdivided as
# B1 | B2
# _  _ _
# B3 | B4
B1 = numpy.zeros(shape=(8,8,3))
B2 = numpy.zeros(shape=(8,8,3))
B3 = numpy.zeros(shape=(8,8,3))
B4 = numpy.zeros(shape=(8,8,3))

# populate B1, B2, B3, B4 with image data
# data stored as RGB, need YCbCr for MPEG-1 processing, convert // later step

B1 = M[0:8,0:8,:]
B2 = M[0:8,8:16,:]
B3 = M[8:16,0:8,:]
B4 = M[8:16,0:8,:]

# for each matrix layer, run 2D DCT
# subsample layers 2,3 by only running 2D DCT on these layers for B1

# for now, Y cooresponds to R layer, Rb to B layer, Rr to G layer

OY1 = dct2(B1[:,:,0]) 
OY2 = dct2(B2[:,:,0]) 
OY3 = dct2(B3[:,:,0]) 
OY4 = dct2(B4[:,:,0]) 
ORb = dct2(B1[:,:,1]) 
ORr = dct2(B1[:,:,2]) 

'''
Quantization steps for each matrix
'''

#define base quantization matrix - taken from IJG standard 
Qb = numpy.matrix('16 11 10 16 24 40 51 61;12 12 14 19 26 58 60 55;14 13 16 24 40 57 69 56;14 17 22 29 51 87 80 62;18 22 37 56 68 109 103 77;24 35 55 64 81 104 113 92;49 64 78 87 103 121 120 101;72 92 95 98 112 100 103 99') 
'''
# from quaity factor, determine multiplication factor for quantization
if Q < 50:
	S = 5000/Q;
else:
	S = 200 - 2*Q;
'''

# determine quantized matrix result
for i in range (0,8):
	for j in range (0,8):
		Qf = Qb[i,j]
		OY1[i,j] = OY1[i,j] // Qf
		OY2[i,j] = OY2[i,j] // Qf
		OY3[i,j] = OY3[i,j] // Qf
		OY4[i,j] = OY4[i,j] // Qf
		ORb[i,j] = ORb[i,j] // Qf
		ORr[i,j] = ORr[i,j] // Qf
		


