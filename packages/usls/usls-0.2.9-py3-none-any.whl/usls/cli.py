import sys
import rich
import re
from omegaconf import OmegaConf, DictConfig
import argparse
from enum import Enum, auto, unique
from rich.panel import Panel
from typing import Dict, List, Union, Optional, Any


from usls import __version__
from usls.src.utils import LOGGER, CONSOLE, IMG_FORMAT, LABEL_FORMAT, VIDEO_FORMAT
# ---------------------------------------------------------------------------------------------
from usls.src.info import run_dir_info
from usls.src.labelling import run_inspect
from usls.src.cleanup import run_cleanup
from usls.src.dir_combine import run_dir_combine
from usls.src.spider import run_spider
from usls.src.rename import run_rename
from usls.src.deduplicate import run_deduplicate
from usls.src.video_tools import run_v2is, run_vs2is, run_play 

# TODO
from usls.src.label_combine import combine_labels
from usls.src.class_modify import class_modify
# ---------------------------------------------------------------------------------------------



def run(opt: DictConfig):
    task_mapping = {
        'info': run_dir_info,
        'dir_combine': run_dir_combine,
        'dir-combine': run_dir_combine,
        'inspect': run_inspect,
        'clean': run_cleanup,
        'cleanup': run_cleanup,
        'clean-up': run_cleanup,
        'spider': run_spider,
        'rename': run_rename,
        'de-duplicate': run_deduplicate,
        'de_duplicate': run_deduplicate,
        'check': run_deduplicate,
        'v2is': run_v2is,
        'vs2is': run_vs2is,
        'play': run_play,
    }.get(opt.task)(opt)





def cli() -> None:

	if len(sys.argv) == 1:
		sys.argv.append('-h')

	args = parse_cli()
	args.update({'task': sys.argv[1]})  # add task
	args = OmegaConf.create(args)
	
	# log
	CONSOLE.print(
		Panel(
			f"[green]{OmegaConf.to_yaml(args)}",
			# f"{args}",
			title='args',
			box=rich.box.ROUNDED
		)
	)

	# run
	run(args) 	



def parse_cli() -> Dict:

	parser = argparse.ArgumentParser(
		prog='usls',
		description='😺 This is a useless toolkits for doing useless things.',
		epilog=f'version: {__version__} '
	)
	parser.add_argument(
		'--version', '-v', '-V', 
		action='version', 
		version=f'version: {__version__}',
		help='get version',
	)

	subparsers = parser.add_subparsers(
		title='Tasks',
		description='👇 Tasks are as follows',
		# help='task sub-commands help'
	)

	# --------------------------
	# 	info parser ✅
	# 	TODO: video info, img info
	# --------------------------
	info_parser = subparsers.add_parser(name='info', help='Directory info')
	info_parser.add_argument(
		'--dir', '-d',
		required=True, type=str, default=None, 
		help='Directory to be inspect'
	)
	info_parser.add_argument(
		'--fmt',
		required=False, type=str, nargs="+", 
		default=IMG_FORMAT + LABEL_FORMAT + VIDEO_FORMAT, 
		help=f'File format. default -> {IMG_FORMAT + LABEL_FORMAT + VIDEO_FORMAT}'
	)
	info_parser.add_argument(
		'--non-recursive',
		required=False, action='store_true', 
		help="Non-recursive, do not iterable all directories"
	)

	# -----------------------------
	# 	dir_combine parser✅
	# -----------------------------
	dir_combine_parser = subparsers.add_parser(
		name='dir-combine', 
		# aliases=['dir_combine'], 
		help='Combine all items in directory'
	)
	dir_combine_parser.add_argument(
		'--input-dir', '--dir', '-d',
		required=True, type=str, default=None, help='Directory to be combined'
	)
	dir_combine_parser.add_argument(
		'--output-dir', '--out',
		required=False, type=str, default='output-conbined', help='Directory saveout'
	)
	dir_combine_parser.add_argument(
		'--fmt',
		required=False, nargs='+', type=str, default=[], 
		help="File format like: .py, .jpg, .txt, .yaml, ..."
	)
	dir_combine_parser.add_argument(
		'--move',
		required=False, action='store_true', 
		help='copy or move, default is copy.'
	)


	# ---------------------
	# 	cleanup parser  ✅
	# ---------------------
	cleanup_parser = subparsers.add_parser(
		name='clean', aliases=['cleanup'], 
		help='Clean-Up of Images & Labels pair'
	)
	cleanup_parser.add_argument(
		'--img-dir', 
		required=True, type=str, default=None, 
		help='image dir'
	)
	cleanup_parser.add_argument(
		'--label-dir',
		required=False, type=str, default=None, 
		help='label dir'
	)
	cleanup_parser.add_argument(
		'--fmt-img',
		required=False, type=str, default=IMG_FORMAT, 
		help=f'image format: {IMG_FORMAT}'
	)	
	cleanup_parser.add_argument(
		'--fmt-label',
		required=False, type=str, default=LABEL_FORMAT, 
		help=f'label format: {LABEL_FORMAT}'
	)
	cleanup_parser.add_argument(
		'--filtered-dir',
		required=False, type=str, default='cleanup-filtered', help='filtered dir'
	)	
	cleanup_parser.add_argument(
		'--keep-empty-label',
		action='store_true', 
		help='keep empty label file or not'
	)
	cleanup_parser.add_argument(
		'--non-recursive',
		required=False, action='store_true', 
		help="Do not iterable all directories"
	)


	# ---------------------
	# 	spider parser  ✅
	# ---------------------
	spider_parser = subparsers.add_parser(
		name='spider', 
		help='Baidu Image Spider'
	)
	spider_parser.add_argument(
		'--words', 
		default='', nargs="+", required=True, type=str, 
		help='Key words'
	)
	spider_parser.add_argument(
		'--output-dir',
		required=False, type=str, default='baidu-image-spider', help='baidu image spider output dir'
	)	

	# ---------------------
	# 	rename parser  ✅
	# ---------------------
	rename_parser = subparsers.add_parser(
		name='rename', 
		help='Rename directory items'
	)
	rename_parser.add_argument(
		'--dir', '-d',
		required=True, type=str, default=None, 
		help='Directory'
	)
	# rename_parser.add_argument(
	# 	'--label-dir',
	# 	required=False, type=str, default=None, 
	# 	help='Label directory, rename IMAGE_FORMAT file in --dir and LABELD_FORMAT files in --label-dir when this one is used.'
	# )
	rename_group = rename_parser.add_mutually_exclusive_group(
		required=True
	)
	rename_group.add_argument(
		'--zero-number', '--znum',
		action='store_true',
		required=False,
		help='number ordered, left padding with N zeros'
	)
	rename_group.add_argument(
		'--number', '--num',
		action='store_true',
		required=False,
		help='number ordered'
	)
	rename_group.add_argument(
		'--random', 
		action='store_true',
		required=False,
		help='random raname'
	)
	rename_group.add_argument(
		'--uuid', '--uuid4', 
		action='store_true',
		required=False,
		help='random raname'
	)
	rename_group.add_argument(
		'--prefix',
		required=False, type=str, default=None, 
		help='prefix-original'
	)


	# --------------------------
	# 	de-duplicator parser  ✅
	# --------------------------
	de_duplicate_parser = subparsers.add_parser(
		name='de-duplicate', aliases=['check'], 
		help='Check image integrity and de-duplicate images'
	)
	de_duplicate_parser.add_argument(
		'--dir', '-d', '--input-dir',
		required=True, type=str, default=None, 
		help='Images Directory'
	)
	de_duplicate_parser.add_argument(
		'--duplicated-dir',
		required=False, type=str, default='duplicated-items', 
		help='Duplicated Items Directory'
	)
	de_duplicate_parser.add_argument(
		'--deprecated-dir',
		required=False, type=str, default='deprecated-items', 
		help='Depracted Items Directory'
	)
	de_duplicate_parser.add_argument(
		'--distance', '--dist',
		required=False, type=int, default=3, 
		help='Based on hash similarity, --dist 3(default)'
	)
	de_duplicate_parser.add_argument(
		'--device',
		required=False, type=int, default=0, 
		help='using cpu/gpu device, --device 0(GPU default)'
	)
	de_duplicate_parser.add_argument(
		'--conf',
		required=False, type=float, default=0.98, 
		help='Based on nn similarity, --conf 0.98(default)'
	)	
	de_duplicate_group = de_duplicate_parser.add_mutually_exclusive_group(
		required=True
	)
	de_duplicate_group.add_argument(
		'--base',
		action='store_true',
		required=False,
		help='Method based on MD5, simple but more accurately.'
	)
	de_duplicate_group.add_argument(
		'--similarity', '--hash',
		action='store_true',
		required=False, 
		help='Method based on hash similarity, with --dist, time-consuming (not recommended)'
	)
	de_duplicate_group.add_argument(
		'--nn',
		action='store_true',
		required=False, 
		help='Method based on nn similarity, with --conf, more faster (recommended)'
	)

	# ---------------------
	# 	v2is parser   ✅
	# ---------------------
	v2is_parser = subparsers.add_parser(
		name='v2is', 
		help='Single video to images'
	)
	v2is_parser.add_argument(
		'--source', '--video', '-v',
		required=True, type=str, default=None, 
		help='Video source input'
	)
	v2is_parser.add_argument(
		'--output-dir',
		required=False, type=str, default='v2is', 
		help='Saveout Directory'
	)	
	v2is_parser.add_argument(
		'--frame', '--interval',
		required=False, type=int, default=10, 
		help='Frame interval'
	)	
	v2is_parser.add_argument(
		'--fmt-img',
		required=False, type=str, default='.jpg', 
		help='Image clipped format'
	)		
	v2is_parser.add_argument(
		'--view',
		action='store_true',
		required=False, 
		help='View when clipping'
	)
	v2is_parser.add_argument(
		'--flip',
		required=False, type=str, default=None,
		choices=['ud', 'lr', 'udlr', 'lrud'],
		help='Flipping video'
	)
	v2is_parser.add_argument(
		'--rotate',
		required=False, type=int, default=None,
		choices=[90, 180, 270],
		help='Counterwise Rotation'
	)

	# ---------------------
	# 	vs2is parser   ✅
	# ---------------------
	vs2is_parser = subparsers.add_parser(
		name='vs2is', 
		help='Videos to images'
	)
	vs2is_parser.add_argument(
		'--dir', '--source', '--video', '-v',
		required=True, type=str, default=None, 
		help='Video source input'
	)
	vs2is_parser.add_argument(
		'--output-dir',
		required=False, type=str, default='vs2is', 
		help='Saveout Directory'
	)	
	vs2is_parser.add_argument(
		'--frame', '--interval',
		required=False, type=int, default=10, 
		help='Frame interval'
	)	
	vs2is_parser.add_argument(
		'--fmt-img',
		required=False, type=str, default='.jpg', 
		help='Image clipped format'
	)		
	vs2is_parser.add_argument(
		'--view',
		action='store_true',
		required=False, 
		help='View when clipping'
	)
	vs2is_parser.add_argument(
		'--flip',
		required=False, type=str, default=None,
		choices=['ud', 'lr', 'udlr', 'lrud'],
		help='Flipping video'
	)
	vs2is_parser.add_argument(
		'--rotate',
		required=False, type=int, default=None,
		choices=[90, 180, 270],
		help='Counterwise Rotation'
	)

	# ---------------------------------
	# 	video play & record parser   ✅
	# ---------------------------------
	play_rec_parser = subparsers.add_parser(
		name='play', 
		help='Play and record single video or stream.'
	)
	play_rec_parser.add_argument(
		'--source', '--video', '-v',
		required=True, type=str, default=None, 
		help='Video source input'
	)
	play_rec_parser.add_argument(
		'--output-dir',
		required=False, type=str, default='video-records', 
		help='Saveout Directory'
	)	
	play_rec_parser.add_argument(
		'--delay',
		required=False, type=int, default=1, 
		help='Keywait'
	)	
	play_rec_parser.add_argument(
		'--fourcc',
		required=False, type=str, default='mp4v', 
		help='Image clipped format'
	)		
	play_rec_parser.add_argument(
		'--no-view',
		action='store_true',
		required=False, 
		help='Do not view while playing'
	)
	play_rec_parser.add_argument(
		'--rec',
		action='store_true',
		required=False, 
		help='Record at the start'
	)
	play_rec_parser.add_argument(
		'--flip',
		required=False, type=str, default=None,
		choices=['ud', 'lr', 'udlr', 'lrud'],
		help='Flipping video'
	)
	play_rec_parser.add_argument(
		'--rotate',
		required=False, type=int, default=None,
		choices=[90, 180, 270],
		help='Counterwise Rotation'
	)


	# ---------------------
	# 	download parser  
	# ---------------------



	# ----------------------------
	# 	label-combine parser  
	# ----------------------------


	# ---------------------
	# 	class-modify parser  
	# ---------------------



	# ---------------------
	# 	inspect parser  ✅
	# ---------------------
	inspect_parser = subparsers.add_parser(
		name='inspect', # aliases=['label-det'], 
		help='Detection labelling'
	)
	inspect_parser.add_argument(
		'--img-dir', '--dir',
		required=True, type=str, default=None, help='image dir'
	)
	inspect_parser.add_argument(
		'--label-dir',
		required=False, type=str, default=None, help='label dir'
	)
	inspect_parser.add_argument(
		'--depreacated-dir', 
		required=False, type=str, default="deprecated-images", help='deprecated image dir'
	)
	inspect_parser.add_argument('--classes', default='', nargs="+", required=True, type=str, help='label classes list')
	inspect_parser.add_argument('--window-width', default=800, type=int, help='opencv windows width')
	inspect_parser.add_argument('--window-height', default=600, type=int, help='opencv windows height')
	inspect_parser.add_argument(
		'--no-qt',
		action='store_true',
		required=False, 
		help='without QT'
	)

	args = vars(parser.parse_args())
	return args




if __name__ == '__main__':
	cli()
