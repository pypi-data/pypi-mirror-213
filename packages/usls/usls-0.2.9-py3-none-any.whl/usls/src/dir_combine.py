
from tqdm import tqdm 
from pathlib import Path
import sys
import rich
import os
import shutil

from omegaconf import OmegaConf, DictConfig
from usls.src.utils import CONSOLE, IMG_FORMAT, VIDEO_FORMAT, LABEL_FORMAT, get_common_files



def dir_combine(
		input_dir,
		output_dir,
		fmt=[],  #
		move=False,
	):

	
	# check if input_dir is dir
	if not Path(input_dir).is_dir():
		raise TypeError(f"{input_dir} is not a dreectory.")


	saveout_dir = Path(output_dir).resolve()
	
	with CONSOLE.status("[bold cyan]Checking saveout directory...") as status:
		# mkdir if now exists OR check if has data in exist dir
		if not saveout_dir.exists():
			saveout_dir.mkdir()
		else:
			for x in saveout_dir.iterdir():
				if x.is_file() or x.is_dir():   # got one file at least
					CONSOLE.print(
						f"Saveout directory: [u green]{saveout_dir}[/u green] [b red]exists[/b red]! And has items!\n"
						f"[b red]Try somewhere else.\n"
						)
					sys.exit()	

	# glob
	with CONSOLE.status("[bold cyan]Checking files...") as status:
		if len(fmt) == 0:
			item_list = [x for x in Path(input_dir).glob("**/*") if x.is_file()]
		else:
			item_list = []
			for s in fmt:
				s = "**/*" + s
				item_list += [x for x in Path(input_dir).glob(s)]


	# combining
	if len(item_list) == 0:
		# raise ValueError(f'No items found to be combined!')
		CONSOLE.print(
			f'[red]Not Found! Go check out: \n[/red]'
			f'directory: [u]{Path(input_dir).resolve()}[/u]\n' 
			f'fmt: {fmt} (empty means all types)'
		)
		saveout_dir.rmdir() # remove saveout directory
		sys.exit()
	else:
		for d in tqdm(item_list, desc='Combining'):
			s = str(d).replace(os.path.sep, '-')
			des_path = saveout_dir.resolve() / s 

			# copy or move
			if move:  
				shutil.move(str(d.resolve()), str(des_path))
			else:
				shutil.copy(str(d.resolve()), str(des_path))
	CONSOLE.print(f"Saved at: [u green]{saveout_dir}")   # saveout log

	

def run_dir_combine(args: DictConfig):
	# called by run.py

	dir_combine(
		input_dir=args.input_dir,
		output_dir=args.output_dir,
		fmt=args.fmt,
		move=args.move
	)


