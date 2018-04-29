import sys
import numpy as np
import proto_mpeg
import encoder
import decoder
import matplotlib.pyplot as plt
import os
import pickle

#Only for test
def compare_block(pic,m,n,QF):
    tmp = pic.getBlock(m,n)
    #print(tmp.shape)
    tmp1 = encode.encode_block(tmp,QF)
    tmp2 = decode.decode_block(tmp1,QF)
    
    plt.figure(figsize=(6,2))
    plt.subplot(121)
    plt.title('Regenerated block QF={}'.format(QF))
    plt.imshow(tmp2)
    plt.subplot(122)
    plt.title('Original block')
    plt.imshow(tmp)
    plt.show()

#Only for test
def compare_pics(pic, QF):
    blocks = []
    for m in range(pic.v_mblocks):
        for n in range(pic.h_mblocks):
            block = pic.getBlock(m,n)
            encoded_block = encode.encode_block(block,QF)
            decoded_block = decode.decode_block(encoded_block,QF)
            blocks.append(decoded_block)
    f=[]
    for m in range(pic.v_mblocks):
        rst = []
        for i in range(16):
            for n in range(pic.h_mblocks):
                block = blocks[m*pic.h_mblocks+n]
                rst+=list(block[i])
        #print(len(rst))
        f+=rst
    #print(len(f))
    f = np.array(f).reshape(pic.v_mblocks*16,pic.h_mblocks*16,3)
    
    plt.figure(figsize=(15,8))
    plt.subplot(121)
    plt.title('Regenerated picture QF={}'.format(QF))
    plt.imshow(f)
    plt.subplot(122)
    plt.title('Original picture')
    plt.imshow(pic.getFrame())
    plt.show()

def compare_compress_rate(fname):
    fullPic = plt.imread(fname)[:32,:64]
    pic = proto_mpeg.Frame(fullPic)

    statinfo = os.stat('./pics/baboon.jpg')
    ori_size = statinfo.st_size

    for QF in [0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5]:
    
        encoded_dre = encode.encode_pic_to_dre(pic,QF) # dre refers to DC_term,Run_level,EOB
        bits = encode.dre_to_bit(encoded_dre)
        
        print('QF = ',QF,', original size = ',ori_size, ', bitstream length = ',len(bits))
