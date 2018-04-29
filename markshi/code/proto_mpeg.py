import numpy as np
import sys
import cv2
import scipy.fftpack as fft
import matplotlib.pyplot as plt
#from encode import encode_block,encode_pic_to_dre
#from decode import decode_block,decode_pic_from_dre

quantization_matrix = np.matrix('16 11 10 16 24 40 51 61;'\
                                '12 12 14 19 26 58 60 55;'\
                                '14 13 16 24 40 57 69 56;'\
                                '14 17 22 29 51 87 80 62;'\
                                '18 22 37 56 68 109 103 77;'\
                                '24 35 55 64 81 104 113 92;'\
                                '49 64 78 87 103 121 120 101;'\
                                '72 92 95 98 112 100 103 99')

# An array of indices that we use to sample a flattened DCT array in zigzag order.
zz_indices = [  0,  1,  8, 16,  9,  2,  3, 10,
               17, 24, 32, 25, 18, 11,  4,  5,
               12, 19, 26, 33, 40, 48, 41, 34,
               27, 20, 13,  6,  7, 14, 21, 28,
               35, 42, 49, 56, 57, 50, 43, 36,
               29, 22, 15, 23, 30, 37, 44, 51,
               58, 59, 52, 45, 38, 31, 39, 46,
               53, 60, 61, 54, 47, 55, 62, 63]

# An reversed array of zz_indices that we use to regenerate matrix
reversed_zz_indices = [ 0,  1,  5,  6, 14, 15, 27, 28,
                        2,  4,  7, 13, 16, 26, 29, 42,
                        3,  8, 12, 17, 25, 30, 41, 43,
                        9, 11, 18, 24, 31, 40, 44, 53,
                       10, 19, 23, 32, 39, 45, 52, 54,
                       20, 22, 33, 38, 46, 51, 55, 60,
                       21, 34, 37, 47, 50, 56, 59, 61,
                       35, 36, 48, 49, 57, 58, 62, 63]

class Frame:
    def __init__(self, image):
        '''
        @param image: RBG image of shape (height, width, 3)
        @param QF: quality factor, normally range from 0.1 to 1.5
        '''
        self.image = image
        self.r = image[:, :, 0]
        self.g = image[:, :, 1]
        self.b = image[:, :, 2]
        self.v_mblocks = np.shape(self.r)[0] // 16
        self.h_mblocks = np.shape(self.r)[1] // 16

    def getFrame(self):
        reconstructed_image = np.dstack((self.r, self.g, self.b))
        return reconstructed_image
        
    def show(self):
        self.getFrame()
        plt.imshow(self.getFrame())
    
    def getBlock(self,m,n):
        m_start = m*16
        n_start = n*16
        tmp = self.image[m_start:m_start+16,n_start:n_start+16]
        #plt.imshow(tmp)
        return tmp