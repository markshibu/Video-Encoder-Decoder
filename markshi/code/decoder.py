import cv2
import os
import numpy as np
import scipy.fftpack as fft
from proto_mpeg import quantization_matrix,zz_indices,reversed_zz_indices,Frame
import matplotlib.pyplot as plt
import matplotlib
import pickle
from PIL import Image

def decode_block(F,QF):
    def zigzag_to_flattened_block(encoded_string):
        """
        @param encoded_string: A list in the form <DC term> <run, level> <EOB>
        @return rst: A zigzag series of coeffs
        """
        rst = [encoded_string[0]]
        for i in encoded_string[1:-1]:
            #print(i)
            for _ in range(i[0]):
                rst.append(0)
            rst.append(i[1])
        #print(16-len(rst))
        for i in range(64-len(rst)):
            rst.append(0)
        return rst

    def de_quantize(F,QF):
        quant_matrix=np.ceil(quantization_matrix*QF)
        quant_matrix[quant_matrix>255]=255
        tmp = []
        for i in range(8):
            for j in range(8):
                #tmp1 = F[i][j]*quant_matrix.A[i][j]
                #print(tmp1)
                tmp.append(int(F[i][j]*quant_matrix.A[i][j]))
        return np.array(tmp).reshape(8,8)

    def idct(y):
        return fft.idct(fft.idct(y, axis=0, norm='ortho', type=2), axis=1, norm='ortho', type=2)

    def regenerate(src8_8):
        """
        @param src8_8: A 8*8 downsampled block 
        @return regenerated_16_16: A 16*16 block, expanding each pixel to 2*2.
        """
        #print(src8_8)
        rst16_16_flattened=[]
        for i in range(8):
            for j in range(8):
                #print(src8_8[i][j])
                rst16_16_flattened.append(src8_8[i][j])
                rst16_16_flattened.append(src8_8[i][j])
            for j in range(8):
                #print(src8_8[i][j])
                rst16_16_flattened.append(src8_8[i][j])
                rst16_16_flattened.append(src8_8[i][j])
        regenerated_16_16 = np.array(rst16_16_flattened).reshape(16,16)
        return regenerated_16_16

    rst = []
    for i in F:
        decoded_F = zigzag_to_flattened_block(i)
        de_flattened_F = np.array([decoded_F[i] for i in reversed_zz_indices]).reshape(8,8)
        de_quantized_F = de_quantize(de_flattened_F,QF)
        regenerated_F = idct(de_quantized_F).astype(int)
        rst.append(regenerated_F)
    Y1,Y2,Y3,Y4,subsample_Cb,subsample_Cr = rst
    rst=[]
    for i in range(8):
        tmp = list(Y1[i])+list(Y2[i])
        rst+=tmp
    #print(rst)
    for i in range(8):
        tmp = list(Y3[i])+list(Y4[i])
        rst+=tmp
    regenerated_Y = np.array(rst).reshape(16,16)
    regenerate_Cb = regenerate(subsample_Cb)
    regenerate_Cr = regenerate(subsample_Cr)
    regenerated_block = cv2.merge((regenerated_Y, regenerate_Cb, regenerate_Cr)).astype(np.uint8)
    regenerated_block = cv2.cvtColor(regenerated_block,cv2.COLOR_YCR_CB2RGB)
    return regenerated_block
    
# dre refers to DC_term,Run_level,EOB
def decode_dre_to_pic(v,h,blocks,QF):
    decoded_blocks = []
    for block in blocks:
        decoded_block = decode_block(block,QF)
        decoded_blocks.append(decoded_block)
    f=[]
    for m in range(v):
        rst = []
        for i in range(16):
            for n in range(h):
                block = decoded_blocks[m*h+n]
                rst+=list(block[i])
        #print(len(rst))
        f+=rst
    #print(len(f))
    f = np.array(f).reshape(v*16,h*16,3)
    return f

def decode_bit_to_dre_1(input):    
    with open(input, "rb") as fp:   # Unpickling
        decoded_dre = pickle.load(fp)
    return decoded_dre

def decode_pic(v,h,input,QF,output="output.jpg"):
    decoded_dre = decode_bit_to_dre_1(input)
    #print(decoded_dre)    
    decoded = decode_dre_to_pic(v,h,decoded_dre,QF)
    #plt.imshow(decoded)
    #plt.show()
    matplotlib.image.imsave(output, decoded)

from PIL import Image
def pics_to_video(fname,fps,output):
    os.system("ffmpeg -r "+str(fps)+" -i "+fname+" -vcodec mpeg4 -y "+output)

def decode_video(input,fps=10,output='decoded_movie.mp4'):
   
    imgs = decode_bit_to_dre_1(input)
    headtag = imgs.pop(0)
    if not headtag == 'EC504':
        print("invalid binary file - must use a file encoded using this project... aborting")
        return None
    numimg = imgs.pop(0)
    QF = imgs.pop(0)
    v = imgs.pop(0)
    h = imgs.pop(0)
    print("Number of Frames: "+str(numimg))
    print("QF: "+str(QF))
    print("decoding start!")
    i=1
    if not os.path.exists("./decoded_pics"):
        os.makedirs("./decoded_pics")
    for img in imgs:
        print("processing img",i)
        tmp = decode_dre_to_pic(v,h,img,QF=QF)
        output1 = "./decoded_pics/output%04d.png" % i
        plt.imsave(output1, tmp, format='png')
        i+=1
    print("decoding done!")
    pics_to_video("./decoded_pics/output%04d.png",fps,output)
    #pics_to_video("./pics/sample_images/scene00%03d.jpg", 24,'original_movie.mp4')