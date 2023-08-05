import numpy as np
from pathlib import Path
import sys
from datetime import datetime
from omegaconf import DictConfig, OmegaConf

from usls.src.nn.ppprocessor import PPProcessor
from usls.src.nn.backends import ORTBackend
from usls.src.nn.utils import MetricType, Device, decode_device, TIMER, ModulesType
from usls.src.utils import download_from_url, FEAT_WEIGHTS_URL
# ----------------------------------------------------------------------------------------------------------------
FILE = Path(__file__).resolve()
ROOT = FILE.parents[3]  


class BaseModule:
    # answer for each backend's runtime stages: pre-process + infer + post-process

    def __init__(self, config: DictConfig):
        self.__dict__.update(config)    # update configs
        self.device = decode_device(self.device)  # decode device
        self.weights = download_from_url(
            FEAT_WEIGHTS_URL, 
            saveout=str(ROOT / ('usls/src/nn/fe-224.onnx')),
            prefix=' nn model'
        )
        # self.weights = str(ROOT / ('usls/src/nn/fe-224.onnx'))

        self.engine = ORTBackend(weights=self.weights, device=self.device)   # build engine
        self.__dict__.update(self.engine.__dict__)  # assgine engine's attrs to module
        self.type = ModulesType[self.type]      # module type: det, cls, kpt, ...
        self.pp_processor = PPProcessor(kwargs=self.__dict__) # build pp-processor
        if self.type is ModulesType.FEAT_EXT:   # update extractor feats dim
            self.feat_dim = self.outputs_shape[0][-1]  
        if self.classes_names is None:  # check if has classes_names
            self.classes_names = {i: f'class-{i}' for i in range(10)}
        self.verbose = False   # for time testing


    def __call__(self, x):
        # inference
        with TIMER('Pre Processing', verbose=self.verbose) as t_pre:
            ims, im0s = self.pp_processor.pre_process(x, size=self.input_size)   # pre-process
        with TIMER('Multi-backends inference', verbose=self.verbose) as t_infer:
            y = self.engine(ims)    # inference
        with TIMER('Post Processing', verbose=self.verbose) as t_post:
            y = self.pp_processor.post_process(y, ims=ims, im0s=im0s)   # post-preocess
        return y


    def _warmup(self, input_shape=None, times=1, batch_size=3):
        # warmup
        if not input_shape:
            input_shape=tuple(self.input_size) + (3,)
        dummy = [np.random.randint(low=0, high=255, size=input_shape)] * batch_size  # , dtype=np.float32)
        for _ in range(times):
            _ = self(dummy)

 
    def destroy(self):
        pass



