import os
from pathlib import Path
from typing import Union

from .const import fps_filename, imgs_dirname, video_formats
from .dataset import Sequence, ImageSequence, VideoSequence

def is_video_file(filepath: str) -> bool:
    return Path(filepath).suffix.lower() in video_formats

def get_fps_file(dirpath: str) -> Union[None, str]:
    fps_file = os.path.join(dirpath, fps_filename)
    if os.path.isfile(fps_file):
        return fps_file
    return None

def get_imgs_directory(dirpath: str, img_dir_name: str = None) -> Union[None, str]:
    if img_dir_name is None:
        imgs_dir = os.path.join(dirpath, imgs_dirname)
    else:
        imgs_dir = os.path.join(dirpath, img_dir_name)
    if os.path.isdir(imgs_dir):
        return imgs_dir
    return None

def get_video_file(dirpath: str) -> Union[None, str]:
    filenames = [f for f in os.listdir(dirpath) if is_video_file(f)]
    if len(filenames) == 0:
        return None
    assert len(filenames) == 1
    filepath = os.path.join(dirpath, filenames[0])
    return filepath

def fps_from_file(fps_file) -> float:
    assert os.path.isfile(fps_file)
    with open(fps_file, 'r') as f:
        fps = float(f.readline().strip())
    assert fps > 0, 'Expected fps to be larger than 0. Instead got fps={}'.format(fps)
    return fps

def get_sequence_or_none(dirpath: str, img_dir_name: str = None, default_fps: int = None) -> Union[None, Sequence]:
    # Can be ImageSequence if there is an imgs directory
    imgs_dir = get_imgs_directory(dirpath, img_dir_name)
    if imgs_dir:
        fps_file = get_fps_file(dirpath)
        if fps_file:
            fps = fps_from_file(fps_file)
        elif default_fps:
            fps = default_fps  # Use default fps if there is no fps file. (only for ImageSequence)
        else:
            return None
        return ImageSequence(imgs_dir, fps)
    
    # Can be VideoSequence if there is a video file.
    video_file = get_video_file(dirpath)
    if video_file:
        fps_file = get_fps_file(dirpath)
        if fps_file:
            fps = fps_from_file(fps_file)
        else:
            fps = None  # Have to use fps from meta data.
        return VideoSequence(video_file, fps)
    
    return None
