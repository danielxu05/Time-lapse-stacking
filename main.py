

import cv2
import glob
import argparse
from tqdm import tqdm

def image2video(nfile, output_file, frames):
    img_array = []
    size = None
    print('loading files...')
    for filename in tqdm(sorted(glob.glob(nfile+'*.jpeg'))):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        #print('load file '+filename)
    print('loaded all files')
    out = cv2.VideoWriter(output_file,cv2.VideoWriter_fourcc(*'DIVX'), frames, size)
     
    print(f'writing to {output_file}....')
    for i in tqdm(range(len(img_array))):
        out.write(img_array[i])
    out.release()
    print('exported.')


def main(args):
    # Access the argument values
    if args.output:
        output = args.output
    else:
        output ='./video.mp4'
    if args.input:
        input = args.input
    if args.frames:
        frames = int(args.frames)
    else:
        frames = 25
    image2video(input, output_file=output, frames = frames)
    
if __name__ == "__main__":
    # Create a parser
    parser = argparse.ArgumentParser(description="stack images to video")

    # Add optional arguments
    parser.add_argument('-o', '--output', help='output nfile')
    parser.add_argument('-i', '--input', help='input file')
    parser.add_argument('-f', '--frames', help='frames per second')
    
    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args)



