import cv2
import os
import yaml
import numpy as np
import onnxruntime
import yaml
from pathlib import Path
import sys
import faiss
from enum import Enum, auto, unique
from dataclasses import dataclass, field
from typing import Union, Any, Optional, List
import contextlib
import inspect
import time
import pynvml
import logging
import rich
from rich.console import Console
import base64
from io import BytesIO
from loguru import logger as LOGGER
# LOGGER.configure(
#     handlers=[
#         dict(sink=sys.stdout, format="[{time:MM-DD HH:mm:ss}] [{level}] --> {message}", level="DEBUG"),
#         # dict(sink="file.log", enqueue=True, serialize=True),
#     ],
#     # levels=[dict(name="NEW", no=13, icon="¤", color="")],
#     # extra={"common_to_all": "default"},
#     # patcher=lambda record: record["extra"].update(some_value=42),
#     # activation=[("my_module.secret", False), ("another_library.module", True)],
# )


CONSOLE = Console()
IMG_FORMAT = ('.bmp', '.jpg', '.jpeg', '.png')
VIDEO_FORMAT = ('.mp4', '.flv', '.avi', '.mov')
STREAM_FORMAT = ('rtsp://', 'rtmp://', 'http://', 'https://')



@unique
class ErrOkType(Enum):
    Ok = 0
    Err = -1


@dataclass
class Result:
    message: str = None
    code: Union[int, ErrOkType] = 0
    data: Any = None


@unique
class ModulesType(Enum):
    DET = 0
    CLS = auto()
    SEG_INST = auto()  
    KPT = auto()
    FEAT_EXT = auto()
    OTHER = auto()


@unique
class MetricType(Enum):
    FlatL2 = 0
    FlatIP = auto()
    IVFFlat = auto()
    IVFPQ = auto()


@unique
class DeviceKind(Enum):
    CPU = 0
    GPU = auto()


@dataclass
class Device:
    id: int = -1
    type: DeviceKind = field(default=DeviceKind.CPU)


def decode_device(device: Union[int, str]='cpu') -> Device:
    # decode str to Device
    # support device='0', device=0, device='cuda:0', device='cpu', device='cuda: 999', device='  cuda: 999 '..
    # not support multi device: device='0,1,2' 

    device = str(device).strip().lower().replace('cuda:', '').replace(' ', '')  # to string, "cuda:1" -> '1'
    is_cpu = device == 'cpu'

    if is_cpu:
        return Device(id=0, type=DeviceKind.CPU)
    elif device:   # cuda: x
        try:
            pynvml.nvmlInit()
            num_gpu = pynvml.nvmlDeviceGetCount()

            # error checking
            if int(device) >= num_gpu:
                raise ValueError(f"GPU device id: {device} is greater than {num_gpu}")
            _d = Device(id=int(device), type=DeviceKind.GPU)
            CONSOLE.print(f"> Using GPU Device: {_d.id}")
            return _d
        except Exception:
            _d = Device(id=-1, type=DeviceKind.CPU)
            CONSOLE.print(f"> No GPU device found! device: {device} -> {_d.type.name}")
            return _d



class CenterCrop:
    def __init__(self, size=224):
        super().__init__()
        self.h, self.w = (size, size) if isinstance(size, int) else size

    def __call__(self, im):  # im = np.array HWC
        imh, imw = im.shape[:2]
        m = min(imh, imw)  # min dimension
        top, left = (imh - m) // 2, (imw - m) // 2
        return cv2.resize(im[top:top + m, left:left + m], (self.w, self.h), interpolation=cv2.INTER_LINEAR)


class Normalize:
    def __init__(self, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
        super().__init__()
        self.mean = mean
        self.std = std

    def __call__(self, x): 
        if not isinstance(self.mean, np.ndarray):
            self.mean = np.array(self.mean, dtype=np.float32)
        if not isinstance(self.std, np.ndarray):
            self.std = np.array(self.std, dtype=np.float32)
        if self.mean.ndim == 1:
            self.mean = np.reshape(self.mean, (-1, 1, 1))
        if self.std.ndim == 1:
            self.std = np.reshape(self.std, (-1, 1, 1))
        _max = np.max(abs(x))
        _div = np.divide(x, _max)  # i.e. _div = data / _max
        _sub = np.subtract(_div, self.mean)  # i.e. arrays = _div - mean
        arrays = np.divide(_sub, self.std)  # i.e. arrays = (_div - mean) / std
        return arrays


class Softmax:
    def __init__(self, dim=1):
        super().__init__()
        self.dim = dim

    def __call__(self, x):
        exp_x = np.exp(x)
        return exp_x / np.sum(exp_x, axis=self.dim)



def scale_boxes_batch(
        boxes, 
        ims_shape, 
        im0s_shape, 
        min_bbox_size=None, 
        masks=False,
        # min_wh_ratio=None
    ):
    # Batch Rescale boxes (xyxy) to original image size

    for i in range(len(boxes)):
        if len(boxes) > 0:
            boxes[i][:, :4] = scale_boxes(ims_shape[i].shape[1:], boxes[i][:, :4], im0s_shape[i].shape[:-1]) # .round()
    
        # min bbox filter
        if min_bbox_size:
            filtered = (boxes[i][:, [2, 3]] - boxes[i][:, [0, 1]] >= min_bbox_size).all(axis=1)
            boxes[i] = boxes[i][filtered]

        if masks:
            boxes[i] = boxes[i][:, :6]

        # if min_wh_ratio:
        #     filtered = ((boxes[i][:, 2] - boxes[i][:, 0]) / (boxes[i][:, 3] - boxes[i][:, 1]) >= min_wh_ratio).all(axis=1)
        
    return boxes


def scale_boxes(img1_shape, boxes, img0_shape, ratio_pad=None):
    # Rescale boxes (xyxy) from img1_shape to img0_shape

    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    boxes[:, [0, 2]] -= pad[0]  # x padding
    boxes[:, [1, 3]] -= pad[1]  # y padding
    boxes[:, :4] /= gain

    # clip boxes
    boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, img0_shape[1])  # x1, x2
    boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, img0_shape[0])  # y1, y2
    return boxes



# @jit
def batched_nms(prediction, *, conf_thres=0.25, iou_thres=0.45, max_det=100, nm=0, v8=False):
    """Non-Maximum Suppression (NMS) on inference results to reject overlapping detections
    Returns:
         list of detections, on (n,6) tensor per image [xyxy, conf, cls]
    """

    if isinstance(prediction, (list, tuple)):  # YOLOv5 model in validation model, output = (inference_out, loss_out)
        prediction = prediction[0]  # select only inference output
    if v8:
        prediction = np.einsum('qwe->qew', prediction)
    bs = prediction.shape[0]  # batch size
    nc = prediction.shape[2] - nm - 4 if v8 else prediction.shape[2] - nm - 5 # number of classes

    if v8:
        mi = 4 + nc  # mask start index
        xc = np.amax(prediction[..., 4:mi], axis=-1) > conf_thres   #  (1, 8400)
    else:
        mi = 5 + nc  # mask start index
        xc = prediction[..., 4] > conf_thres  # candidates    # (1, 25200)


    assert 0 <= conf_thres <= 1, f'Invalid Confidence threshold {conf_thres}, valid values are between 0.0 and 1.0'
    assert 0 <= iou_thres <= 1, f'Invalid IoU {iou_thres}, valid values are between 0.0 and 1.0'

    # Settings
    max_wh = 7680  # (pixels) maximum box width and height
    max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()
    time_limit = 0.5 + 0.05 * bs  # seconds to quit after
    t = time.time()
    output = [np.zeros((0, 6 + nm), dtype=np.float32)] * bs

    for xi, x in enumerate(prediction):  # image index, image inference
        x = x[xc[xi]]  # confidence

        # If none remain process next image
        if not x.shape[0]:
            continue

        if not v8:
            x[:, 5:] *= x[:, 4:5]  # conf = obj_conf * cls_conf

        # Box/Mask
        box = xywh2xyxy(x[:, :4])  # center_x, center_y, width, height) to (x1, y1, x2, y2)
        mask = x[:, mi:]  # zero columns if no masks

        # Detections matrix nx6 (xyxy, conf, cls)
        if v8:
            conf, j = x[:, 4:mi].max(1, keepdims=True), x[:, 4:mi].argmax(1, keepdims=True).astype('float32')
        else:
            conf, j = x[:, 5:mi].max(1, keepdims=True), x[:, 5:mi].argmax(1, keepdims=True).astype('float32')
        x = np.concatenate((box, conf, j, mask), 1)[conf.reshape(-1) > conf_thres]


        # Check shape
        n = x.shape[0]  # number of boxes
        if not n:  # no boxes
            continue
        elif n > max_nms:  # excess boxes
            x = x[np.argsort(-x[:, 4][:max_nms])]
        else:
            x = x[np.argsort(-x[:, 4])]

        # Batched NMS
        c = x[:, 5:6] * max_wh  # classes
        boxes, scores = x[:, :4] + c, x[:, 4]  # boxes (offset by class), scores
        i = nms_vanil(boxes, scores, iou_thres)  # NMS

        # limit detections
        if i.shape[0] > max_det:  
            i = i[:max_det]
        output[xi] = x[i]

        # timer limits
        if (time.time() - t) > time_limit:
            CONSOLE.print("NMS time limit exceeded!")
            break  # time limit exceeded
    return output



def nms_vanil(boxes, scores, threshold):
    # vanilla nms

    boxes_area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
    keep_indices = []
    indices = scores.argsort()[::-1]
    while indices.size > 0:
        i = indices[0]
        keep_indices.append(i)
        w = np.maximum(0, np.minimum(boxes[:, 2][i], boxes[:, 2][indices[1:]]) - np.maximum(boxes[:, 0][i], boxes[:, 0][indices[1:]]))
        h = np.maximum(0, np.minimum(boxes[:, 3][i], boxes[:, 3][indices[1:]]) - np.maximum(boxes[:, 1][i], boxes[:, 1][indices[1:]]))
        intersection = w * h
        ious = intersection / (boxes_area[i] + boxes_area[indices[1:]] - intersection) 
        indices = indices[np.where(ious <= threshold)[0] + 1]
    return np.asarray(keep_indices)



def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y



def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, ratio, (dw, dh)




class TIMER(contextlib.ContextDecorator):
    """Timer"""
    def __init__(
        self, 
        description='', 
        verbose=True
    ):
        self.verbose = verbose
        self.description = f'[{description}]' if description != '' else ''


    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.duration = time.time() - self.t0
        if self.verbose:
            print(f"> TIMER::duration {self.description} --> {(time.time() - self.t0) * 1e3:.2f} ms.")


    def __call__(self, obj):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            ret = obj(*args, **kwargs)
            if self.verbose:
                print(f"> TIMER::duration {self.description} --> {(time.time() - t0) * 1e3:.2f} ms.")
            return ret
        return wrapper


def image_to_base64(image_data):
    image = cv2.imencode('.jpg', image_data)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code


def base64_to_image(src):
    try:
        image_stream = BytesIO()
        image_stream.write(base64.b64decode(src))
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        image_data = cv2.imdecode(file_bytes, 1)
        return image_data
    except Exception as e:
        print('Cause of error :{}'.format(e))
        return 'Error:{}'.format(e)
