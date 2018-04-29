import cv2
import numpy as np
import scipy.fftpack as fft
from proto_mpeg import quantization_matrix,zz_indices,reversed_zz_indices, Frame
import matplotlib.pyplot as plt
from huffman import EOF,make_encoder_table
import pickle

def encode_block(src,QF):
    """
    @param src: A 16*16*3 block
    @return encoded_string: A list of 6 lists of encoded pairs for each block in [Y1,Y2,Y3,Y3,subsampled_Cb,subsampled_Cr]. 
                            in the form [<DC term> <run, level> <EOB>] 
    """
    def subsample(src):
        """
        @param src: A 16*16 block
        @return rst: 8*8 subsampled blcok, with mean of each 2x2 block
        """
        rst = []
        for i in range(0,len(src),2):
            for j in range(0,len(src),2):
                rst.append(np.mean([src[i][j],src[i][j+1],src[i+1][j],src[i+1][j+1]]))
        rst = np.array(rst)
        rst = rst.reshape(8,8).astype(np.uint8)
        return rst

    def quantize(F,QF):
        quant_matrix=np.ceil(quantization_matrix*QF)
        #print(quant_matrix)
        quant_matrix[quant_matrix>255]=255
        #print(F,quant_matrix)
        return (F/quant_matrix).astype(np.int)

    def run_level(tmp):
        """
        process the middle part -- <run, level>
        @param tmp: A list of numbers
        @return encoded_string: A list of <run, level> pair
        """
        def prefix_0(s):
            """
            @param s: A series of integers
            @return count: Number of prefix 0s
            """
            if len(s)==0:
                return 0
            i, count = 0, 0
            while s[i]==0 :
                count += 1
                if i==len(s)-1:
                    return count
                i+=1
            return count

        encoded_string = []
        while True:
            a = prefix_0(tmp)
            if a==len(tmp):
                break
            encoded_string.append((a,tmp[a]))
            tmp = tmp[a+1:]
        return encoded_string

    def zigzag_from_flattened_block(tmp):
        """
        @param tmp: A zigzag series of coeffs
        @return encoded_string: A list, in the form <DC term> <run, level> <EOB>
        """
        encoded_string = [tmp[0]]
        encoded_string += run_level(tmp[1:])
        encoded_string.append('EOB')
        return encoded_string    

    def dct(y):
        return fft.dct(fft.dct(y, axis=0, norm='ortho', type=2), axis=1, norm='ortho', type=2)

    def encode(F):
        dct2_F = dct(F)
        qtz_F = quantize(dct2_F,QF)
        zz_series = [qtz_F.A1[i] for i in zz_indices]
        encoded = zigzag_from_flattened_block(zz_series)
        return encoded

    YCrCb = cv2.cvtColor(src, cv2.COLOR_RGB2YCR_CB)
    Y,Cb,Cr = cv2.split(YCrCb)

    # split and subsample
    Y1 = Y[:8,:8]
    Y2 = Y[:8,8:]
    Y3 = Y[8:,:8]
    Y4 = Y[8:,8:]
    subsample_Cb = subsample(Cb)
    subsample_Cr = subsample(Cr)
    
    # encode each 8*8 block and return
    return [encode(Y1), encode(Y2), encode(Y3), encode(Y4),
            encode(subsample_Cb), encode(subsample_Cr)]


# dre refers to DC_term,Run_level,EOB
def encode_pic_to_dre(pic,QF):
    blocks = []
    for m in range(pic.v_mblocks):
        for n in range(pic.h_mblocks):
            block = pic.getBlock(m,n)
            encoded_block = encode_block(block,QF)
            blocks.append(encoded_block)
    return blocks


from bitstring import BitArray, BitStream, Bits, ReadError
def dre_to_bit(blocks):
    encoder_table = make_encoder_table()
    #print(BitArray('0b001')==BitArray('0b1')) # >>>False
    #print(table)
    #print(len(blocks))
    def translate_block(block):
        #print(len(block),block)
        rst = BitArray();
        for mblock_88 in block:
            #print(mblock_88[0],bin(mblock_88[0]))

            # Encode the DC term into a BitArray
            encoded_bits = BitArray(bin(mblock_88[0]))
            #print(encoded_bits)

            # Encode the AC terms
            for j in range(1,len(mblock_88)-1):
                # Note only positive levels are stored in encoder table.
                run_level = mblock_88[j]
                run_level_positive = tuple(map(abs, run_level))
                if run_level_positive in encoder_table:
                    to_append = encoder_table[run_level_positive]
                    #print(mblock_88[j],run_level_positive,to_append)
                    encoded_bits.append(to_append)
                    #print(mblock_88[j][1])
                    # Check to see if the level is negative, write appropriate sign bit.
                    if mblock_88[j][1]<0:
                        encoded_bits.append('0b1')
                    else:
                        encoded_bits.append('0b0')
                else:
                    # The run_level combo was not fond in the encoder table. We will do the following:
                    # i) encode an escape character
                    # ii) encode a 6-bit unsigned integer for the run, which is at most 62
                    # iii) encode a 16-bit signed integer for the level
                    encoded_bits.append(encoder_table['ESC'])
                    run = 'uint:6=' + str(run_level[0])
                    level = 'int:16=' + str(run_level[1])
                    encoded_bits.append(run)
                    encoded_bits.append(level)
                    #print("else not exist")
            encoded_bits.append(encoder_table['EOM'])
            #print(encoded_bits)
            rst.append(encoded_bits)
        rst.append(encoder_table['EOB'])
        return rst

    rst = BitArray();
    for block in blocks:
        translated_block = translate_block(block)
        #print(translated_block)
        rst.append(translated_block)
    return rst

def dre_to_bit_1(blocks,output):
    with open(output, "wb") as fp:   #Pickling
        pickle.dump(blocks, fp)

def encode_pic(input,QF,output="output.bin"):
    fullPic = plt.imread(input)
    pic = Frame(fullPic)
    encoded_dre = encode_pic_to_dre(pic,QF)
    dre_to_bit_1(encoded_dre,output)

def encode_video(img_list,QF,output="output.bin"):
    print("encoding start!")
    first_img = img_list[0]
    fullPic = plt.imread(first_img)
    headtag = 'EC504'
    numimg = len(img_list)
    pic = Frame(fullPic)
    v = pic.v_mblocks
    h = pic.h_mblocks

    rst = [headtag, numimg, QF,v,h]
    for img in img_list:
        print("processing ",img)
        fullPic = plt.imread(img)
        pic = Frame(fullPic)
        encoded_dre = encode_pic_to_dre(pic,QF)
        rst.append(encoded_dre)
    dre_to_bit_1(rst,output)
    print("encoding done!")