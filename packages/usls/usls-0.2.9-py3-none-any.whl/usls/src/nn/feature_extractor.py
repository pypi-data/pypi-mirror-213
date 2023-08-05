import cv2
import sys
import numpy as np
from pathlib import Path
from omegaconf import DictConfig, OmegaConf
import rich
from typing import Union, List, Dict, Optional
import faiss
import weakref

# ------------------------------------------
from usls.src.nn.utils import (
	MetricType, TIMER, LOGGER, CONSOLE, IMG_FORMAT, 
	Device, decode_device, DeviceKind, Result, ErrOkType
)
from usls.src.nn.base_module import BaseModule
from usls.src.nn.dataloader import DataLoader




class FEModel:
	"""upper-body detector + clothing extractor + index search""" 

	def __init__(self, *, config: str, do_warmup=False, device=0):

		# configs
		o_conf = OmegaConf.load(config)
		o_conf_cli = OmegaConf.from_cli()
		for k, v in o_conf_cli.items():
			OmegaConf.update(o_conf, k, v, merge=True)
		# o_conf_det = OmegaConf.merge(o_conf.commons, o_conf.modules.detector)
		o_conf_ext = OmegaConf.merge(o_conf.commons, o_conf.modules.extractor)
		self.commons = o_conf.commons   # common attrs
		if device:
			self.commons.device = device
			o_conf_ext.device = device

		self.device = decode_device(self.commons.device)

		# build modules
		# self.detector = BaseModule(o_conf_det)
		self.extractor = BaseModule(o_conf_ext)
		self.modules = dict(
			# det=weakref.proxy(self.detector),
			ext=weakref.proxy(self.extractor)
		)

		# build feats lib
		self.index = faiss.IndexFlatIP(self.extractor.feat_dim)  # from stratch
		# CONSOLE.log(f'> index build from stratch.')

		# do warmup
		if do_warmup:
			self.warmup(times=self.commons.warmup_times, batch_size=self.commons.opt_batch_size)

		# feats labels
		self.feats_labels = []  # coressponding to the input index(feat), when remove some feats in index, remove coressponding labels here 


	def warmup(self, times=1, batch_size=2):
		'''warmup'''
		for t in range(times):
			with TIMER(f"Warmup-{t} | batch={batch_size}", verbose=True):
				for module_name, module in self.modules.items():
					module._warmup(batch_size=batch_size)


	def index_device_synchronized(self, *, device: Device):
		'''set index to gpu devices, when do query'''
		if device.type is DeviceKind.GPU:
			res = faiss.StandardGpuResources()  # single GPU
			self.index = faiss.index_cpu_to_gpu(res, device.id, self.index)
		print(f"> Index synchronized: {device}")


	@property
	def num_feats(self):
		"""number of feats"""
		return self.index.ntotal



	def register(
		self, 
		*,
		xs: List[Union[str, np.ndarray]],   # clipped upper-body
		# ys: List[str],
		# save_index=True,   # TODO: need save label at the same time
	) -> Result:
		"""extract feats & update index"""

		# error checking
		# if not all((isinstance(xs, list), isinstance(ys, list))):
		# 	raise TypeError(f"Type of images: {type(xs)} and labels: {type(ys)} must be list.")
		# if len(xs) != len(ys):
		# 	raise ValueError(f"length of images: {len(xs)} is not equal with length of labels: {len(ys)}.")

		# to np.ndarray if not 
		if not isinstance(xs[0], np.ndarray):
			imgs = list()
			for idx, x in enumerate(xs):
				try:
					_img = cv2.imread(str(x))
				except Exception as E:
					CONSOLE.log(f'Image can no be read: {xs[idx]} | Exception: {E}')
				else:
					imgs.append(_img)
			xs = imgs

		feats = self.extractor(xs) 	# (n, dim)   
		self.index.add(feats)    # update index 
		# self.feats_labels.extend(ys)   # udpate index labels
		nf = feats.shape[0]

		# check again
		# if len(xs) != len(ys):
		# 	raise ValueError(f"length of images: {len(xs)} is not equal with length of labels: {len(ys)}.")

		# self.index_device_synchronized(device=self.device)   # index device sync



	def __call__(self, x: List[np.ndarray], topk=1):

		D, I = self.index.search(y_q, topk)  # query 
		conf, cls_ = D[0][0], self.feats_labels[I[0][0]] 
		# CONSOLE.log(f'conf: {conf} | cls_: {cls_} | path: {imgs_path[idx]}')






# ----------------------------------------------------------------------------------------------------
def main():
	with TIMER('build model') as t_build:
		model = FEModel(config='usls/src/nn/config.yaml', do_warmup=False)
		# model.warmup(times=5, batch_size=2)   # manully


	a = cv2.imread('/mnt/z/Desktop/DTdYQZLYdIDShstp.jpg')
	q = cv2.imread('/mnt/z/Desktop/DFaeQHSEfyEaYZLf.jpg')
	y = model.register(xs=[a,])  # using det
	ll = [
		'/mnt/z/Desktop/DTdYQZLYdIDShstp.jpg',
		# '/mnt/z/Desktop/DFaeQHSEfyEaYZLf.jpg'
	]
	y = model.register(xs=ll)  # using det

	print(model.num_feats)
	

	y_q = model.extractor([q])

	D, I = model.index.search(y_q, 1)  # query 
	print(D)
	print(I)


	exit()

	# 1. register => build feats lib   batch_size=all
	imgs, imgs_np, imgs_ids, imgs_path = [], [], [], []
	for d in [x for x in Path('assets/images/collections').iterdir() if x.is_dir()]:
		[(
			imgs.append(str(x)), 
			imgs_np.append(cv2.imread(str(x))),
			imgs_ids.append(d.stem),
			imgs_path.append(d),
		) for i, x in enumerate(d.iterdir()) if x.suffix in ['.jpg', '.jpeg', '.png']]

	with TIMER('registering') as t_build:
		y = model.register(xs=imgs_np, ys=imgs_ids, use_det=True)  # using det
		# CONSOLE.log(y)
	CONSOLE.log(f"avg: {t_build.duration / model.num_feats} ms")
	
	
	# for k, v in zip(imgs_np, imgs_ids):    # rigister batch_size=1
	# 	model.register(xs=[k], ys=[v], use_det=True)


	# [optional] Append some features even when feats lib already has built.
	# imgs_appends = [
	# 	'assets/images/query/0.png',
	# 	'assets/images/query/1.png',
	# 	'assets/images/query/2.png',
	# ]
	# model.register(xs=imgs_appends, ys=['query', 'query', 'query']) 
	# CONSOLE.log(model.num_feats)

	# pipeline test
	model.index_device_synchronized(device=model.device)
	querys = [str(x) for x in Path('assets/images/query').iterdir()]
	
	coords_q = []
	for idx, x in enumerate(querys):
		img_ = cv2.imread(x)
		coords_q.append({0: [0, 0, img_.shape[1], img_.shape[0]]})   # {0: [0, 0, 2000, 2000], 1: [0, 0, 2000, 2000]}

	y = model(
		[cv2.imread(x) for x in querys], 
		coords=coords_q,
		imgs_path=querys
	)  


	# data_0 = model.index.reconstruct(0)
	# data_1 = model.index.reconstruct(1)
	# data_2 = model.index.reconstruct(2)
	# data_3 = model.index.reconstruct(3)
	# data_129 = model.index.reconstruct(129)

	# remove test
	# rich.print(f'before remove: {len(model.feats_labels)}')
	# model.remove(ids=[1, 0, 5])
	# rich.print(f'after remove: {len(model.feats_labels)}')
	# rich.print(model.feats_labels)


	# new_data_0 = model.index.reconstruct(0)
	# new_data_1 = model.index.reconstruct(1)
	# new_data_2 = model.index.reconstruct(2)
	# new_data_3 = model.index.reconstruct(3)

	# new_data_126 = model.index.reconstruct(126)

	# print(f"data_2 == new_data_0: {(data_2 == new_data_0).all()}")
	# print(f"data_3 == new_data_1: {(data_3 == new_data_1).all()}")
	# print(f"data_129 == new_data_126: {(data_129 == new_data_126).all()}")
	# print(f"data_129 == new_data_127: {(data_129 == model.index.reconstruct(127)).all()}")
	# # a = model.index.index.reconstruct(0)
	# # rich.print(a)

	# sys.exit()

	# # TODO: re-assign id


	# 2. query checking
	# source = [
	# 	'assets/images/query/9.png',
	# 	'assets/images/query/5.png',
	# ]
	# ys_q = model.extractor([cv2.imread(x) for x in source]) 	# extract
	# D, I = model.query(xq=ys_q, topk=5, normalize=True)   # query
	# model.results(D, I, list_queries=source, list_collections=model.feats_labels) 



	# # exit()

	# 3. ensembale query
	# source = [
	# 	# 'assets/images/query/2.png',
	# 	# 'assets/images/query/12.jpg',
	# 	# 'assets/images/query/blue.png',
	# 	# 'assets/images/query/gray.png',
	# 	# 'assets/images/7.jpg',
	# 	# "rtsp://admin:zfsoft888@192.168.0.223:554/h265/ch1/",
	# 	# "rtsp://admin:zfsoft888@192.168.2.223:554/cam/realmonitor?channel=1&subtype=0",
	# 	# "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8",

	# ]
	# y = model([cv2.imread(x) for x in source])  



	# 4. test detector
	# source = "/mnt/z/Desktop/MLOPS/DATASETS/CUSTOM/Clothing/Codes/clothing-code/assets/images/collections"
	# source = "rtsp://admin:zfsoft888@192.168.0.223:554/h265/ch1/"
	# source = 'assets/images/collections'
	# dataloader = DataLoader(source=source, batch_size=1, vid_stride=10)
	# for idx, (path, im0, vid_cap, msg) in enumerate(dataloader):
	# 	with TIMER(f"{idx}-th cost:", verbose=True):
	# 		ys = model.detector(im0)
	# 	rich.print(ys)

	# 	for idx, y in enumerate(ys):  
	# 		for *xyxy, conf, cls_ in reversed(y):
	# 			cv2.rectangle(im0[idx], (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0,255,0), 2, cv2.LINE_AA)  # filled
	# 			cv2.putText(
	# 				im0[idx],
	# 				f'{model.detector.classes_names[cls_]}: {conf:.2f}', 
	# 				(int(xyxy[0]), int(xyxy[1])),
	# 				0,
	# 				0.7,
	# 				(0, 255, 0),
	# 				thickness=1,
	# 				lineType=cv2.LINE_AA
	# 			)

	# 			cv2.imshow('demo' + f'{idx}', im0[idx])
	# 			key = cv2.waitKey(0)
	# 			if key == 27:
	# 				cv2.destroyAllWindows()
	# 				return



if __name__ == "__main__":
	main()


