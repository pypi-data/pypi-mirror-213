from pathlib import Path
import rich
from omegaconf import OmegaConf, DictConfig
from datetime import datetime
from typing import Dict, List

from usls.src.utils import CONSOLE, IMG_FORMAT, VIDEO_FORMAT, LABEL_FORMAT



def check_file(
        directory, 
        *, 
        fmt=None, 
        recursive=True
    ) -> (List, Dict):
    # error checking
    if not Path(directory).is_dir():
        raise TypeError(f'{Path(directory)} should be directory, not {type(directory)}')

    # get items
    f_list, f_dict = list(), dict()
    _scope = '**/*' if recursive else '*'

    for x in Path(directory).glob(_scope):
        if x.is_file:
            if fmt is None:
                f_list.append(x)

                if x.suffix == '':
                    f_dict.setdefault(x.stem, []).append(x)
                else:
                    f_dict.setdefault(x.suffix.lower()[1:], []).append(x)
            else:
                if x.suffix.lower() in fmt:
                    f_list.append(x)
                    # f_dict.setdefault(x.suffix.lower()[1:], []).append(x)
                    if x.suffix == '':
                        f_dict.setdefault(x.stem, []).append(x)
                    else:
                        f_dict.setdefault(x.suffix.lower()[1:], []).append(x)
                    
    return f_list, f_dict






def dir_info(
        directory,
        *,
        fmt=None,
        recursive=True,
        title='',
        caption='',
    ) -> None:

    if fmt == IMG_FORMAT + LABEL_FORMAT + VIDEO_FORMAT:
        image_list, image_dict = check_file(directory, fmt=IMG_FORMAT, recursive=recursive)
        label_list, label_dict = check_file(directory, fmt=LABEL_FORMAT, recursive=recursive)
        video_list, video_dict = check_file(directory, fmt=VIDEO_FORMAT, recursive=recursive)
    else:
        f_list, f_dict = check_file(directory, fmt=fmt, recursive=recursive)


    # display
    table = rich.table.Table(
        title=title, 
        title_style='left',
        box=rich.box.ASCII,   # box.MARKDOWN ,SIMPLE   , rich.box.ASCII2
        show_lines=False, 
        show_header=False,
        caption=caption,
        caption_justify='center',
        # header_style='bold cyan',
        # show_footer=True,
    )
    # table.add_column(
    #     header="Type", 
    #     footer='',
    #     justify="left", 
    #     # style="b", 
    #     no_wrap=False
    # )
    # table.add_column(
    #     header="Count", 
    #     justify="right", 
    #     # style="b green", 
    #     no_wrap=False
    # )
    # table.add_column(
    #     header="Details", 
    #     justify="left", 
    #     # style="b green", 
    #     no_wrap=False
    # )

    if fmt == IMG_FORMAT + LABEL_FORMAT + VIDEO_FORMAT:
        details_images = {'.' + k: len(v) for k, v in image_dict.items()}
        details_labels = {'.' + k: len(v) for k, v in label_dict.items()}
        details_videos = {'.' + k: len(v) for k, v in video_dict.items()}

        # content
        table.add_row(f"Directory", f"{Path(directory).resolve()}", end_section=True)
        table.add_row(f"IMAGES", f"{details_images}", f"{len(image_list)}", end_section=False)
        table.add_row(f"LABELS", f"{details_labels}", f"{len(label_list)}", end_section=False)
        table.add_row(f"VIDEOS", f"{details_videos}", f"{len(video_list)}", end_section=False)
    else:
        details_files = {'.' + k: len(v) for k, v in f_dict.items()}
        table.add_row(f"Directory", f"{Path(directory).resolve()}", end_section=True)
        table.add_row(f"FILES", f"{details_files}", f"{len(f_list)}", end_section=False)
    CONSOLE.print(table)





def run_dir_info(args: DictConfig):
    # called by run.py

    with CONSOLE.status("[bold green]Working on Directory INFO...") as status:
        dir_info(
            directory=args.dir,
            fmt=args.fmt,
            recursive=not args.non_recursive,
            title='DIR INFO',
            caption=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        )


