import argparse
from os import listdir, path
import sys
import numpy as np
import proto_mpeg
import encode
import decode
import matplotlib.pyplot as plt

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

def main():
    #img_name = 'night.jpg'
    #fullPic = plt.imread(img_name)
    QF=0.5
    img_name = 'baboon.jpg'
    fullPic = plt.imread(img_name)[:32,:64]
    pic = proto_mpeg.Frame(fullPic)
    encoded_dre = encode.encode_pic_to_dre(pic,QF) # dre refers to DC_term,Run_level,EOB
    encode.dre_to_bit(encoded_dre)
    #print(len(encoded_dre))
    #decoded = decode.decode_pic_from_dre(pic,encoded_dre,QF)
    #plt.imshow(decoded)
    #plt.show()

    # Compare encoded and then decoded block with the original block, using different QF ranging from 0.1-1.5
    #for QF in [0.1,0.3,0.5,0.7,1,1.2,1.5]:compare_block(pic,0,0,QF)
    # Compare encoded and then decoded full picture with the original picture, using different QF ranging from 0.1-1.5
    #for QF in [0.1,0.3,0.5,0.7,1,1.2,1.5]:compare_pics(pic,QF)

    """
    parser = argparse.ArgumentParser(description='EC504 proto-mpeg encoder for jpeg images')
    parser.add_argument('--out', nargs=1, default=['output.bin'], help='filename of encoded file. default is output.bin')
    parser.add_argument('--alg', nargs=1, choices=['n', 'fd', 'bm'], default=['n'], help='temporal compression algorithm. n=none; fd=frame difference; bm=block matching. Default is none.')
    parser.add_argument('--qf', nargs=1, type=int, choices=[1, 2, 3, 4], default=[1], help='quantization factor for HF suppression. Default is 1. Higher values achieve higher compression.')
    parser.add_argument('--limit', nargs=1, type=int, help='cap the number of images that will be encoded. Default is no limit (all files).')
    parser.add_argument('input', nargs=argparse.REMAINDER, help='Either a single directory or a list of files to encode, separated by spaces.')

    args = parser.parse_args()

    # Print help if no arguments are given
    if (len(sys.argv[1:])) == 0:
        parser.print_help()
        parser.exit()

    # Handle output filename argument
    outname = args.out[0]

    # Handle source location (either a directory or a list of files)
    if args.input == []:
        # If not given any files for the input argument
        print("No input files given. Use -h to see help.")
        parser.exit()
    else:
        # try to read directory at input[0]. If this fails, assume we have a list of one or more files.
        try:
            filenames = sorted(listdir(args.input[0]))
            # Listdir will work without a trailing '/', but the code that follows won't. Append it if it is missing.
            if args.input[0][-1] != '/':
                args.input[0] = args.input[0] + '/'
            files = [args.input[0] + fname for fname in filenames]
            if len(args.input) > 1:
                print("Warning: additional parmeters for <input> that follow a directory are ignored. Use -h to see help.")
        except NotADirectoryError:
            files = args.input
        finally:
            files = [file for file in files if file.endswith('.jpg') or file.endswith('.jpeg')]
            if len(files) == 0:
                print("No jpeg files found.")
                parser.exit()

    # Handle limit on number of files
    if args.limit != None and len(files) > args.limit[0]:
        files = files[:args.limit[0]]

    # Translate algorithm selection
    if args.alg[0]=='n':
        method='none'
    elif args.alg[0]=='fd':
        method='frame_difference'
    elif args.alg[0]=='bm':
        method='block_matching'

    print("Encoding", len(files), "files into", outname, "with motion algorithm", method, "and QF =", args.qf[0])
    proto_mpeg_x.encodeVideo(outname, files, mot_est=method, QF=args.qf[0])

    # Calculate original file size
    original_size_B = 0
    for file in files:
        original_size_B += path.getsize(file)

    #Calculate compressed file size
    compressed_size = path.getsize(outname)

    print("Sum of input image sizes:", '%.2f' % (original_size_B/1e6), 'MB')
    print("Compressed video size:", '%.2f' % (compressed_size/1e6), 'MB')
    print("Compression ratio: %.3f" % (original_size_B/compressed_size))
    """
if __name__ == "__main__":
    main()