import cv2
from pathlib import Path
import numpy as np
import rich
import shutil
import argparse
import os
from tqdm import tqdm
import sys
import random
import time
import logging
import glob
import re
import rich
from rich.console import Console
from datetime import datetime
import contextlib
import numpy as np
from dataclasses import dataclass
from typing import Union
from PIL import ExifTags, Image, ImageOps
import hashlib
from loguru import logger as LOGGER
import uuid
import urllib.request



CONSOLE = Console()
IMG_FORMAT = ('.jpg', '.jpeg', '.png', '.bmp')
LABEL_FORMAT = ('.txt', '.xml', '.yaml', '.csv')
VIDEO_FORMAT = ('.mp4', '.flv', '.avi', '.mov')
ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
FEAT_WEIGHTS_URL = 'https://github.com/jamjamjon/assets/releases/download/usls/fe-224.onnx'


def download_from_url(url, saveout, prefix=''):

    # check saveout 
    if Path(saveout).exists() and Path(saveout).is_file():
        # print(f'{saveout} is already exists, return None.')
        return saveout
    else:
        # urllib.request.urlretrieve(str(url), filename=str(saveout))
        with urllib.request.urlopen(url) as source, open(saveout, "wb") as output:
            with tqdm(
                desc='downloading',
                total=int(source.info().get("Content-Length")),
                ncols=100,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as loop:
                while True:
                    buffer = source.read(8192)
                    if not buffer:
                        break
                    output.write(buffer)
                    loop.update(len(buffer))

        # print(f'{saveout} downloaded!')
        return saveout


def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_md5(f):
    m = hashlib.md5(open(f,'rb').read())
    return m.hexdigest()


def gen_random_string(length):
    return ''.join(random.choices(ASCII_LETTERS, k=length))


def get_common_files(
        directory,
        *,
        fmt=None,
        sort_=True
    ):

    # file list
    f_list = list()
    for x in Path(directory).iterdir():
        if fmt is None:  # get all files, hidden file excluded.
            if str(x).startswith('.'):   # hidden file, leave it
                continue
            elif x.suffix == '':   # no suffix
                if x.is_dir():
                    f_list.append(x)    # dir, append
                else:
                    continue
            else:
                f_list.append(x)    # has suffix, append
        else:  # get specific format file
            if x.suffix in fmt:
                f_list.append(x)


    if sort_:
        f_list.sort(key=natural_sort)    

    return f_list


def verify_images(path, output_dir):
    _check_again = True  # flag

    # PIL check 1st, and restore corrupt JPEG
    try: 
        with Image.open(path) as im:
            im.verify()   # PIL image quality check

            # jpg & jpeg corrupt check
            if im.format.lower() in ('jpeg', 'jpg'):
                with open(path, "rb") as f:
                    f.seek(-2, 2)
                    if f.read() != b'\xff\xd9':     # corrupt JPEG
                        ImageOps.exif_transpose(Image.open(path)).save(path, 'JPEG', subsampling=0, quality=100)
                        CONSOLE.log(f"Corrupt JPEG restored and saved | {path}")
    except OSError:
        CONSOLE.log(f"PIL verify failed! | {path}")
        shutil.move(str(path), str(output_dir))
        _check_again = False  # set flag
        # integrity = False
        return False


    # opencv check again
    if _check_again:
        try:
            if cv2.imread(str(path)) is None:  # get md5 of each image
                shutil.move(str(path), str(output_dir))
                return False
        except Exception as e:
            CONSOLE.log(f"opencv exceptions: {e} | {path}")
            return False

    return True



def natural_sort(x, _pattern=re.compile('([0-9]+)'), mixed=True):
    return [int(_x) if _x.isdigit() else _x for _x in _pattern.split(str(x) if mixed else x)]




# img_list & label_list, relative path
def load_img_label_list(img_dir, label_dir, img_format, info=True):
    image_list = [x for x in Path(img_dir).iterdir() if x.suffix in img_format]
    label_list = list(Path(label_dir).glob("*.txt"))
    
    if info:
        rich.print(f"[green]> Images count: {len(image_list)}")
        rich.print(f"[green]> Labels count: {len(label_list)}")
        

    return image_list, label_list



# img_path => label_path(txt)
def get_corresponding_label_path(img_path, output_dir):
    label_name = Path(img_path).stem + '.txt'
    saveout = Path(output_dir) / label_name 
    return str(saveout)




class TIMER(contextlib.ContextDecorator):

    def __init__(self, prefix='Inspector', verbose=True):
        self.prefix = prefix
        self.verbose = verbose


    def __enter__(self):
        self.t0 = time.time()
        return self


    def __exit__(self, type, value, traceback):
        self.duration = time.time() - self.t0
        if self.verbose:
            print(f"[{self.prefix}] --> {(time.time() - self.t0) * 1e3:.2f} ms.")


    def __call__(self, func):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            ret = func(*args, **kwargs)
            if self.verbose:
                print(f"[{self.prefix}] --> {(time.time() - t0) * 1e3:.2f} ms.")

            return ret
        return wrapper




class Palette:
    """colors palette"""

    def __init__(self, shuffle=False):
        _hex_colors = [
            '33FF00', '9933FF', 'CC0000', 'FFCC00', '99FFFF', '3300FF',
            'FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', 
            '1A9334', '00D4BB', '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', 
            '520085', 'CB38FF', 'FF95C8', 'FF37C7', '#F0F8FF', '#4682B4', '#0000CD', '#9932CC',  
            '#FFB6C1', '#FFC0CB', '#DC143C', '#FFF0F5', '#DB7093', '#FF69B4', '#FF1493', '#C71585',  
            '#DDA0DD', '#EE82EE', '#FF00FF', '#FF00FF', '#8B008B', '#800080', '#BA55D3', '#9400D3',   
            '#8A2BE2', '#9370DB', '#7B68EE', '#6A5ACD', '#483D8B', '#E6E6FA', '#F8F8FF', '#0000FF', 
            '#00008B', '#000080', '#4169E1', '#6495ED', '#B0C4DE', '#778899', '#708090', '#1E90FF', 
            '#87CEFA', '#87CEEB', '#00BFFF', '#808080', '#696969', '#000000', '#DA70D6', '#D8BFD8', 
            '#ADD8E6', '#B0E0E6', '#5F9EA0', '#F0FFFF', '#E1FFFF', '#AFEEEE', '#00FFFF', '#00FFFF', 
            '#008B8B', '#008080', '#48D1CC', '#20B2AA', '#40E0D0', '#7FFFAA', '#00FA9A', '#F5FFFA',  
            '#2E8B57', '#F0FFF0', '#90EE90', '#98FB98', '#8FBC8F', '#32CD32', '#00FF00', '#228B22',  
            '#7FFF00', '#7CFC00', '#ADFF2F', '#556B2F', '#6B8E23', '#FAFAD2', '#FFFFF0', '#FFFFE0',  
            '#BDB76B', '#FFFACD', '#EEE8AA', '#F0E68C', '#FFD700', '#FFF8DC', '#DAA520', '#FFFAF0',  
            '#FFE4B5', '#FFA500', '#FFEFD5', '#FFEBCD', '#FFDEAD', '#FAEBD7', '#D2B48C', '#DEB887',
            '#FAF0E6', '#CD853F', '#FFDAB9', '#F4A460', '#D2691E', '#8B4513', '#FFF5EE', '#A0522D', 
            '#FF4500', '#E9967A', '#FF6347', '#FFE4E1', '#FA8072', '#FFFAFA', '#F08080', '#BC8F8F', 
            '#A52A2A', '#B22222', '#8B0000', '#800000', '#FFFFFF', '#F5F5F5', '#DCDCDC', '#D3D3D3', 
            '#191970', '#9932CC', '#00CED1', '#2F4F4F', '#C0C0C0', '#A9A9A9', '#CD5C5C', '#FF0000',
            '#FFA07A', '#FF7F50', '#FFE4C4', '#FF8C00', '#FDF5E6', '#F5DEB3', '#FFFF00', '#808000',
            '#008000', '#006400', '#00FF7F', '#3CB371', '#4B0082',
        ]
        
        # shuffle color 
        if shuffle:
            random.shuffle(_hex_colors)

        self.palette = [self.hex2rgb(c) if c.startswith('#') else self.hex2rgb('#' + c) for c in _hex_colors]
        self.n = len(self.palette)


    def __call__(self, i, bgr=False):    
        """ int -> rgb color """    
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod  
    def hex2rgb(h):
        """
        int('CC', base=16) hex -> 10
        RGB的数值 = 16 * HEX的第一位 + HEX的第二位
        RGB: 92, 184, 232 
        92 / 16 = 5余12 -> 5C
        184 / 16 = 11余8 -> B8
        232 / 16 = 14余8 -> E8
        HEX = 5CB8E8
        """
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))



def smart_path(path='', *, exist_ok=False, sep='-', mkdir=False, method=0):
    # Increment file or directory path

    # random string in currnet path
    if path == '':
        if method == 0:
            _ASCII_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            path = Path.cwd() / (''.join(random.choices(_ASCII_LETTERS, k=8)))
        elif method == 1:
            path = Path.cwd() / str(uuid.uuid4())
        elif method == 2:
             path = Path.cwd() / datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = Path(path)  # os-agnostic

    # make increment
    if path.exists() and not exist_ok:
        path, suffix = (path.with_suffix(''), path.suffix) if path.is_file() else (path, '')

        # increment path
        for n in range(2, 9999):
            p = f'{path}{sep}{n}{suffix}'  
            if not os.path.exists(p):  # non-exist will break
                break
        path = Path(p)

        # path, suffix = (path.with_suffix(''), path.suffix) if path.is_file() else (path, '')
        # dirs = glob.glob(f"{path}{sep}*")  # similar paths
        # matches = [re.search(rf"%s{sep}(\d+)" % path.stem, d) for d in dirs]
        # i = [int(m.groups()[0]) for m in matches if m]  # indices
        # n = max(i) + 1 if i else 2  # increment number
        # path = Path(f"{path}{sep}{n}{suffix}")  # increment path

    # make dir directly
    if mkdir:
        path.mkdir(parents=True, exist_ok=True)  # make directory


    return path





class SmartDir:

    def __init__(
            self, 
            path,
            # *, 
        ):
        self.path = Path(path)



    def file_type(self):
        # hidden file
        # executable file
        # normal file
        ...


    def info(self):
        # parse dir info
        ...

    def clean_empty_dir():
        ...


    def get_file_by_fmt(self):
        ...


    def combine(self):
        ...


    def rename_content(self):
        # rename 
        ...


    def cleanup(self):
        # clean up dir
        ...


    def de_duplicate(self):
        # de-duplicate
        ...


