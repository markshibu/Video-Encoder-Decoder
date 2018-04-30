import proto_mpeg
import encoder
import decoder
import os
import time
import matplotlib.pyplot as plt

def analyze(QF,n):
    t_start = time.time()
    encode_time = 0
    decode_time = 0
    for i in ["%03d" % i for i in range(n+1)][1:]:

        img_name = './pics/sample_images/scene00'+i+'.jpg'
        print("processing ",img_name)
        fullPic = plt.imread(img_name)
        pic = proto_mpeg.Frame(fullPic)
        v=pic.v_mblocks
        h=pic.h_mblocks
        
        # Encode
        start = time.time()
        encoded_dre = encoder.encode_pic_to_dre(pic,QF) # dre refers to DC_term,Run_level,EOB
        #print(encoded_dre)
        bits = encoder.dre_to_bit_1(encoded_dre,'out.bin')
        encode_time += time.time()-start
        
        # Decode
        start = time.time()
        decoded_dre = decoder.decode_bit_to_dre_1('out.bin')
        #print(decoded_dre)
        decoded = decoder.decode_dre_to_pic(v,h,decoded_dre,QF)
        decode_time += time.time()-start

    print("QF = ",QF)
    print("average total time: ", (time.time()-t_start)/n)
    print("average encode time: ",encode_time/n)
    print("average decode time: ",decode_time/n)




def main():
    for QF in [0.1,0.5,1.0,1.5]:
        analyze(QF=QF, n=3)
    
if __name__ == "__main__":
    main()