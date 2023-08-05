import numpy as np
import onnxruntime
import cv2
import yaml
from pathlib import Path
import rich
import sys
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm

from usls.src.nn.utils import MetricType, Device, decode_device, CenterCrop, Normalize, Softmax, DeviceKind


class ORTBackend:
    def __init__(
        self,
        *,
        weights,
        device: Device,
        max_gpu_mem=None,
    ):
        self.device = device
        self.max_gpu_mem = max_gpu_mem

        # create Runtime session
        providers = [
            # ('CUDAExecutionProvider', {
            #     'device_id': self.device.id,
            #     'arena_extend_strategy': 'kNextPowerOfTwo',
            #     'gpu_mem_limit': self.max_gpu_mem * (1 << 30), 
            #     'cudnn_conv_algo_search': 'EXHAUSTIVE',
            #     'do_copy_in_default_stream': True,
            # } if self.max_gpu_mem is not None else {'device_id': self.device.id}
            # ),
            'CUDAExecutionProvider',
            'CPUExecutionProvider'
        ] if self.device.type is DeviceKind.GPU else ['CPUExecutionProvider']

        # session_options = onnxruntime.SessionOptions()
        # session_options.enable_profiling=True
        self.session = onnxruntime.InferenceSession(weights, providers=providers)  # create session
        self.io_binding = self.session.io_binding()  # io_binding 
        self.i_names = [x.name for x in self.session.get_inputs()]     # only deal with single input for now!
        self.input_shape = self.session.get_inputs()[0].shape
        self.input_size = self.input_shape[-2:]
        self.o_names = [x.name for x in self.session.get_outputs()]
        self.outputs_shape = [x.shape for x in self.session.get_outputs()]   # multi outputs [[1, 25200, 117], [1, 32, 160, 160]],
        
        # get onnx meta
        meta = self.session.get_modelmeta().custom_metadata_map  
        self.classes_names = eval(meta['names']) if 'names' in meta else None

        # init device mem
        self.ort_x, self.ort_y = None, [None] * len(self.outputs_shape)     # .shape()




    def __call__(self, x):
        # y = self.session.run(self.o_names, {self.i_names[0]: x})
        # return y
        # print('---> ', y[0].shape)


        # create input & output ort value
        if self.ort_x is None or x.shape != self.ort_x.shape():

            # pre-allocate cuda io mem
            self.ort_x = onnxruntime.OrtValue.ortvalue_from_numpy(
                numpy_obj=x, 
                device_type='cpu' if self.device.type is DeviceKind.CPU else 'cuda', 
                device_id=self.device.id
            )
            self.ort_y = [onnxruntime.OrtValue.ortvalue_from_shape_and_type(
                shape=self.ort_x.shape()[:1] + self.outputs_shape[i][1:],
                element_type=x.dtype, 
                device_type='cpu' if self.device.type is DeviceKind.CPU else 'cuda', 
                device_id=self.device.id
            ) for i in range(len(self.ort_y))]
        else:  # update input ort value
            self.ort_x.update_inplace(x)   

        # io binding
        self.io_binding.bind_ortvalue_input(self.i_names[0], self.ort_x)
        for i in range(len(self.outputs_shape)):
            self.io_binding.bind_ortvalue_output(self.o_names[i], self.ort_y[i])

        # run & return
        self.session.run_with_iobinding(self.io_binding)  
        # y = [self.ort_y[i].numpy() for i in range(len(self.ort_y))]
        # print(y[0].shape)

        # exit()
        # return y
        return [self.ort_y[i].numpy() for i in range(len(self.ort_y))]







    