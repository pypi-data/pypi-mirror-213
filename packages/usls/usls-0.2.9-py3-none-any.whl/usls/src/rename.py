from pathlib import Path
import rich
from omegaconf import OmegaConf, DictConfig
from datetime import datetime
from typing import Dict, List
import random
import uuid

from usls.src.utils import (
    CONSOLE, IMG_FORMAT, VIDEO_FORMAT, LABEL_FORMAT, 
    gen_random_string, get_common_files, natural_sort
)




def rename(
        directory, 
        *,
        prefix=None,
        with_num=False,
        with_znum=False,
        with_random=False,
        with_uuid=False,
        # label_directory=None,
    ):
    # dir will be rename at the same time, but the items wthin directories will not be renamed.


    # file list
    f_list = get_common_files(directory)

    
    num_file = len(f_list)
    CONSOLE.print(f"Find {num_file} files (hidden files and non-suffixed files are excluded).")


    # with uuid4
    if with_uuid:
        random_strings = set()

        while len(random_strings) != num_file:
            random_strings.add(str(uuid.uuid4()))

        for x, x_ in zip(f_list, random_strings):
            x.rename(x.with_stem(x_))


    # random 
    if with_random:
        bits = 16   # 2 bytes
        random_strings = set()
        
        while len(random_strings) != num_file:
            random_strings.add(gen_random_string(bits))
        
        for x, x_ in zip(f_list, random_strings):
            x.rename(x.with_stem(x_))


    # with num & znum & random letters
    if with_num or with_znum or prefix:

        # with prefix concatenation first
        if prefix:
            for x in f_list:
                x.rename(x.with_stem(prefix + '-' + x.stem))
        else:
            for x in f_list:
                x.rename(x.with_stem('j1a2m3j4a5m6j7o8n9' + '-' + x.stem))          

        # ordered number
        if with_num:  
            idx = 0
            for x in get_common_files(directory):
                x.rename(x.with_stem(str(idx)))
                idx += 1 

        # ordered number - zero_padding
        if with_znum:
            idx = 0
            bits = len(str(num_file))
            for x in get_common_files(directory):
                x.rename(x.with_stem(str(idx).zfill(bits)))
                idx += 1
    

    CONSOLE.print(f"Task Complete ✅")



def run_rename(args: DictConfig):
    # called by run.py
    with CONSOLE.status("[bold green]Renaming...") as status:
        rename(
            directory=args.dir,
            prefix=args.prefix,
            with_num=args.number,
            with_znum=args.zero_number,
            with_random=args.random,
            with_uuid=args.uuid,
            # label_directory=args.label_dir,
        )


