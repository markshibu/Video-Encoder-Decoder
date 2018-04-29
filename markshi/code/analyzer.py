import proto_mpeg
import encode
import decode
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
        
        # Encode
        start = time.time()
        encoded_dre = encode.encode_pic_to_dre(pic,QF) # dre refers to DC_term,Run_level,EOB
        #print(encoded_dre)
        bits = encode.dre_to_bit_1(encoded_dre)
        encode_time += time.time()-start
        
        # Decode
        start = time.time()
        decoded_dre = decode.decode_bit_to_dre_1(bits)
        #print(decoded_dre)
        decoded = decode.decode_dre_to_pic(pic,decoded_dre,QF)
        decode_time += time.time()-start

    print("QF = ",QF)
    print("average total time: ", (time.time()-t_start)/n)
    print("average encode time: ",encode_time/n)
    print("average decode time: ",decode_time/n)


def pics_to_video(fname,output):
    os.system("ffmpeg -r 24 -i "+fname+" -vcodec mpeg4 -y "+output+".mp4")

def main():
    #pics_to_video('./pics/sample_images/scene00%03d.jpg', 'original_movie')
    analyze(QF=1, n=3)
    
if __name__ == "__main__":
    main()