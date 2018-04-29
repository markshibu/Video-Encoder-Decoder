import argparse
import sys
import numpy as np
import proto_mpeg
import encoder
import decoder
import matplotlib.pyplot as plt
import os
import pickle
import comparer

def main():
    fname = "./pics/sample_images/scene00001.jpg"
    fullPic = plt.imread(fname)
    pic = proto_mpeg.Frame(fullPic)
    v,h = pic.v_mblocks,pic.h_mblocks # 22,40

    QF=0.1
    #encode.encode_pic(fname,QF=QF,output="output.bin")
    #decode.decode_pic(v,h,input="output.bin",QF=QF,output="./decoded_pics/night.jpg")

    img_list = ["./pics/sample_images/scene00%03d.jpg" % i for i in range(10)][1:]
    #print(img_list)

    encoder.encode_video(img_list,QF=QF,output="output.bin")
    decoder.decode_video(input="output.bin",output='decoded_movie.mp4')

    #fname = "./decoded_pics/output0001.jpg"
    #fullPic = plt.imread(fname)
    #print(fullPic.shape)

    #### Compare
    #comparer.compare_compress_rate('./pics/baboon.jpg')
    #for QF in [0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5]: comparer.compare_block(pic,0,0,QF)
    #for QF in [0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5]: comparer.compare_pics(pic,QF)


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
            filenames = sorted(os.listdir(args.input[0]))
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
        original_size_B += os.path.getsize(file)

    #Calculate compressed file size
    compressed_size = os.path.getsize(outname)

    print("Sum of input image sizes:", '%.2f' % (original_size_B/1e6), 'MB')
    print("Compressed video size:", '%.2f' % (compressed_size/1e6), 'MB')
    print("Compression ratio: %.3f" % (original_size_B/compressed_size))
    """
if __name__ == "__main__":
    main()