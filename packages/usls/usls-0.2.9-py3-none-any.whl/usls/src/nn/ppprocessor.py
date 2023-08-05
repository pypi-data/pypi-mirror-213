import numpy as np
from pathlib import Path
import cv2
import sys


# modules
from usls.src.nn.utils import (
    CenterCrop, Softmax, Normalize, letterbox, ModulesType, 
    scale_boxes_batch, xywh2xyxy, TIMER, batched_nms
)

 
class PPProcessor:
    # pre-post processor

    def __init__(self, *, kwargs):

        # get all vars in order to align args in pre-process() & post-process()
        self.type = kwargs.get('type', None)
        if not self.type and self.type not in ModulesType:  # module type checking
            raise TypeError(f"{self.type} not in supported type: {ModulesType.__members__.keys()}")
        self.conf_threshold = kwargs.get('conf_threshold', .5)
        self.iou_threshold = kwargs.get('iou_threshold', .4)    # fixed basically 
        self.min_bbox_size = kwargs.get('min_bbox_size', None)
        self.classes_names = kwargs.get('classes_names', None)
        self.input_size = kwargs.get('input_size', None)
        self.use_center_crop = kwargs.get('use_center_crop', False)  # default not using
        self.feat_dim = kwargs.get('dim', 512)  # extractor
        self.v8 = kwargs.get('v8_nms', False)


        # pre-post-process function mapping
        self.func_mapping = {
            'pre': {
                ModulesType.DET: self._pre_det,
                ModulesType.CLS: self._pre_cls,
                ModulesType.FEAT_EXT: self._pre_feat_ext,
                ModulesType.OTHER: self._pre_other

            },
            'post': {
                ModulesType.DET: self._post_det,
                ModulesType.CLS: self._post_cls,
                ModulesType.FEAT_EXT: self._post_feat_ext,
                ModulesType.OTHER: self._post_other
            }
        }


    def __set_name__(self, owner, func_name):
        pass    


    def pre_process(self, x, size):

        # error checking
        assert isinstance(x, list), "--> Input images must be a list!" 
        assert len(x) > 0, "--> Input images is empty!"

        # preprocess
        im_list, im0_list = [], []
        for image in x:
            im, im0 = self._pre_process_single_image(image, size)   # pre-process single image
            im_list.append(im)
            im0_list.append(im0)
        return np.concatenate(im_list, 0), im0_list  # (batch, 3, size, size ), original image list(np.ndarray)



    def post_process(self, x, *, ims=None, im0s=None):
        # x: output of backends inference
        # ims: stacks of original images after pre-processed
        # im0s: original images list
        return self.func_mapping['post'][self.type](
            x,
            ims=ims,
            im0s=im0s
        )



    def _pre_process_single_image(self, x, size):

        if isinstance(x, (str, np.ndarray)):
            # read image if it is not ndarray
            if isinstance(x, str):   
                x = cv2.imread(x)
            assert isinstance(x, np.ndarray), f'Image type should be np.ndarray'
            return self.func_mapping['pre'][self.type](x, size)     # pre-process for all types of models
        else:
            sys.exit(f'Type of element in Input image list is wrong! ---> {x}')


    def _pre_cls(self, x, size):
        # default pre-process for classifier, support override

        if self.use_center_crop:
            y = CenterCrop(size)(x)  # crop
        else:
            y = cv2.resize(x, (size, size) if isinstance(size, int) else size, interpolation=cv2.INTER_LINEAR)   # only resize
        y = np.ascontiguousarray(y.transpose((2, 0, 1))[::-1]).astype(dtype=np.float32) / 255.0 # HWC to CHW -> BGR to RGB -> contiguous 
        y = Normalize()(y)
        y = y[None] if len(y.shape) == 3 else y     # add batch dim
        return y, x


    def _pre_feat_ext(self, x, size):
        # default pre-process for feature extractor, support override

        if self.use_center_crop:
            y = CenterCrop(size)(x)  # crop
        else:
            y = cv2.resize(x, (size, size) if isinstance(size, int) else size, interpolation=cv2.INTER_LINEAR)   # only resize
        y = np.ascontiguousarray(y.transpose((2, 0, 1))[::-1]).astype(dtype=np.float32) / 255.0 # HWC to CHW -> BGR to RGB -> contiguous 
        y = Normalize()(y)
        y = y[None] if len(y.shape) == 3 else y     # add batch dim
        return y, x


    def _pre_det(self, x, size):
        # default pre-process for detector, support override

        with TIMER('letter_box', verbose=False):
            y, _, (pad_w, pad_h) = letterbox(x, new_shape=size, auto=False) 

        with TIMER('HWC to CHW -> BGR to RGB -> Contiguous', verbose=False):
            y = np.ascontiguousarray(y.transpose((2, 0, 1))[::-1]).astype(dtype=np.float32) / 255.0 # HWC to CHW -> BGR to RGB -> contiguous 
            y = y[None] if len(y.shape) == 3 else y
        return y, x


    def _pre_other(self, x, size):
        pass



    def _post_det(self, x, ims, im0s):
        # make sure ims and im0s is not None
        assert ims is not None and im0s is not None, f"`ims` and `im0s` should all be assigned when do detection!"
        y = batched_nms(
            x[0],
            conf_thres=self.conf_threshold, 
            iou_thres=self.iou_threshold,
            nm=0,
            v8=self.v8
        )
        y = scale_boxes_batch(
            y, 
            ims_shape=ims, 
            im0s_shape=im0s, 
            min_bbox_size=self.min_bbox_size,
        )  # de-scale & min-bbox filter
        return np.asarray(y, dtype=object)    # TODO: cost much time   dtype=np.float32


    def _post_cls(self, x, ims=None, im0s=None):
        res = []
        for i, x_ in enumerate(x[0]):
            prob = Softmax(dim=0)(x_)
            if max(prob) < self.conf_threshold:
                res.append([])
            else:
                pred_cls = np.argmax(prob)
                res.append([pred_cls, self.classes_names[pred_cls], prob[pred_cls]])   # TODO: re-name 
        return np.asarray(res, dtype=object)  # numpy.ndarray


    def _post_feat_ext(self, x, ims=None, im0s=None):
        # return x[0] # single output
        return np.divide(x[0], np.sqrt(np.sum(np.square(x[0]), axis=1, keepdims=True)))  # normalize, IP
        # return np.asarray(x[0], dtype=np.ndarray)  # numpy.ndarray


    def _post_other(self, x, size):
        pass