from pathlib import Path
import rich
from omegaconf import OmegaConf, DictConfig
import sys
from tqdm import tqdm
import shutil
import os

from usls.src.utils import CONSOLE, IMG_FORMAT, VIDEO_FORMAT, LABEL_FORMAT
from usls.src.info import check_file, dir_info




def cleanup_images_labels(
        img_dir,
        label_dir,
        filtered_dir,
        fmt_img=IMG_FORMAT,
        fmt_label=LABEL_FORMAT,
        keep_empty_label=False,
        recursive=True
    ):     
    
    # get image & label list
    label_dir = label_dir if label_dir else img_dir
    image_list, _ = check_file(img_dir, fmt=fmt_img, recursive=recursive)
    label_list, _ = check_file(label_dir, fmt=fmt_label, recursive=recursive)


    # get other file 
    f_img_dir_list, _ = check_file(img_dir, fmt=None, recursive=recursive)
    f_label_dir_list, _ = check_file(label_dir, fmt=None, recursive=recursive)
    f_other_list = list(set(f_img_dir_list + f_label_dir_list) - set(image_list) - set(label_list))
    

    # display before 
    table = rich.table.Table(
        title='\n', 
        # title_style='bold cyan',
        box=rich.box.ASCII2, 
        show_lines=False, 
        caption=f"before\n",
        caption_justify='center',
        # header_style='bold',
        # caption_style='cyan',
        show_header=False,
    )

    table.add_row(f"Directory(IMAGES)", f"{Path(img_dir).resolve()}", end_section=False)
    table.add_row(f"Directory(LABELS)", f"{Path(label_dir).resolve()}", end_section=True)
    table.add_row(f"IMAGES", f"{len(image_list)}", end_section=False)
    table.add_row(f"LABELS", f"{len(label_list)}", end_section=False)
    table.add_row(f"OTHERS", f"{len(f_other_list)}", end_section=False)
    CONSOLE.print(table)


    CONSOLE.log(f"Loading files... ✅")


    # make filtered dir
    filtered_dir = Path(filtered_dir)
    if not filtered_dir.exists():
        filtered_dir.mkdir()
    else:
        for x in filtered_dir.iterdir():
                if x.is_dir() or x.is_file():
                    CONSOLE.log(
                            f"Saveout(filtered_dir) directory: [u green]{filtered_dir}[/u green] [b red]exists[/b red]! And has items!\n"
                            f"[b red]Try somewhere else.\n"
                    )
                    sys.exit()

    CONSOLE.log(f"Checking directory... ✅")


    # keep empty label
    if not keep_empty_label:
        # for x in tqdm(label_list, desc='Not Keeping Empty'):
        for x in label_list:
            if Path(x).stat().st_size == 0:
                label_list.remove(x)
                shutil.move(str(x), str(filtered_dir.resolve()))
        CONSOLE.log(f"Filtering empty files... ✅")


    # into dict
    dict_img = {Path(x).stem: x for x in image_list}
    dict_label = {Path(x).stem: x for x in label_list}

    # get common keys
    common_key = set(dict_img.keys()) & set(dict_label.keys())

    
    # get images & labels to be delete
    image_list_to_keep, label_list_to_keep = [], [] 
    for k in common_key:
        image_list_to_keep.append(dict_img.pop(k))
        label_list_to_keep.append(dict_label.pop(k))

    # get images & labels to keep
    image_list_to_delete, label_list_to_delete = list(dict_img.values()), list(dict_label.values())

    # checking
    assert len(image_list_to_keep) == len(label_list_to_keep), f"Images left({len(image_list_to_keep)}) is not equal to label left({len(label_list_to_keep)})."
    CONSOLE.log(f"Matching files... ✅")


    # remove un-matched images & labels & other file
    [shutil.move(str(x), str(filtered_dir.resolve())) for x in image_list_to_delete]
    [shutil.move(str(x), str(filtered_dir.resolve())) for x in label_list_to_delete]
    [shutil.move(str(x), str(filtered_dir.resolve())) for x in f_other_list] 
    CONSOLE.log(f"Coping with un-matched files... ✅")


    # info
    if len([x for x in filtered_dir.glob('**/*')]) == 0:
        filtered_dir.rmdir()
        CONSOLE.log(f"😃 Nothing changed! All images are perfectly matched with labels!")
    else:
        CONSOLE.log(f"Files filtered are saved at: [u green]{filtered_dir.resolve()}")

    # left files    
    CONSOLE.log(f"Files(image) matched are saved at: [u green]{Path(img_dir).resolve()}")
    CONSOLE.log(f"Files(label) matched are saved at: [u green]{Path(label_dir).resolve()}")
    CONSOLE.log(f"Clean-Up complete ✅")



    # display after 
    table = rich.table.Table(
        title='\n', 
        # title_style='bold cyan',
        box=rich.box.ASCII2, 
        show_lines=False, 
        caption=f"after\n",
        caption_justify='center',
        # header_style='bold',
        # caption_style='',
        show_header=False,
    )


    table.add_row(f"Directory(IMAGES)", f"{Path(img_dir).resolve()}", end_section=False)
    table.add_row(f"Directory(LABELS)", f"{Path(label_dir).resolve()}", end_section=True)
    table.add_row(f"IMAGES", f"{len(image_list_to_keep)}", end_section=False)
    table.add_row(f"LABELS", f"{len(label_list_to_keep)}", end_section=False)
    CONSOLE.print(table)





def run_cleanup(args: DictConfig):

    # in case of other keys input
    while True: 
        _input = CONSOLE.input(
            prompt=f"🤔 Sure to do [b green]clean-up[/b green]?\n> "
        )

        # check input
        if _input.lower() in ('n', 'no', 'false', 'f', 'bu', 'gun'):
            CONSOLE.log(f"Cancelled ❌")
            sys.exit()
        elif _input.lower() in (
                'y', 'yes', 'true', 't', 'of course', 'yeah', 
                'enen', 'en', 'shide', 'shi', 'dui', 'ok', 'go',
                'haode', 'duide'
            ):
            with CONSOLE.status("[bold green]Working on clean-up...") as status:
                cleanup_images_labels(
                    img_dir=args.img_dir,
                    label_dir=args.label_dir,
                    filtered_dir=args.filtered_dir,
                    fmt_img=args.fmt_img,
                    fmt_label=args.fmt_label,
                    keep_empty_label=args.keep_empty_label,
                    recursive=not args.non_recursive
                )
            break
