import os
def main():
    os.system("ffmpeg -r 20 -i scene00%03d.jpg -vcodec mpeg4 -y movie.mp4")
if __name__ == "__main__":
    main()