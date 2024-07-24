import argparse
import os
# Must be set before importing torch.
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
# os.environ["CUDA_VISIBLE_DEVICES"] = '0'  # recommend to set this in bash environment variable 'CUDA_VISIBLE_DEVICES=0 python ...'

from utils import Upsampler


def get_flags():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help='Path to input directory. See README.md for expected structure of the directory.')
    parser.add_argument("--output_dir", required=True, help='Path to non-existing output directory. This script will generate the directory.')
    parser.add_argument("--img_dir_name", required=False, help='Spcify the name of the directory containing images. Default is "imgs".')
    parser.add_argument("--fps", type=float, required=False, help='Spcify the default fps of the image sequence if there is no fps file.')
    args = parser.parse_args()
    return args


def main():
    flags = get_flags()

    upsampler = Upsampler(input_dir=flags.input_dir, output_dir=flags.output_dir, img_dir_name=flags.img_dir_name, fps=flags.fps)
    upsampler.upsample()


if __name__ == '__main__':
    main()
