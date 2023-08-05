import argparse
import os
import re
import cv2
import numpy as np
from tqdm import tqdm
from pathlib import Path
import sys
import shutil
import random
import time
import rich
from omegaconf import OmegaConf, DictConfig
from typing import List, Union, Dict, Optional
from enum import Enum, auto
from dataclasses import dataclass, field

from usls.src.utils import (
    Palette, IMG_FORMAT, CONSOLE, natural_sort,
    smart_path
)



# help message
HELP_MSG = '''
Usage:
    ESC:                    Quit 
    r/R:                    Switch mode between Mark and Read
    a(A)/d(D):              Last or next image
    w(W)/s(S):              Last or next label classes
    -/+:                    Adjust line thickness
    t/T:                    Switch line thickness between thickness=1 and thickness=current
    n/N:                    Hide all bboxes' labels
    b/B:                    Blink the bboxes & labels
    l/L:                    Shuffle bbox colors randomly
    i/I:                    Display current image info
    0-8:                    Show bboxes classes-correspondingly
    9:                      Show all bboxes
    delete:                 - way 1. press `c/C` to remove all bboxes and delete label file.
                            - way 2. right button click on bbox in MARK mode. And label
                            file will not be deleted.
    select bbox:            press r/R, then double click one bboxes to select it.
    change bbox's class:    select bbox first, then press `w/s` to change it's class. 
'''

# class ShapeDraw(Enum):
#     # TODO:

#     rect = 0
#     circle = auto()
#     line = auto()
#     polygon = auto()
#     pencil = auto()  


class InspectMode(Enum):
    read = 0
    mark_dets = auto()     # two points --> text file
    mark_kpts = auto()     # multi points --> text file
    doodle = auto()         #  ----> nothing


@dataclass
class Point:
    x: Union[int, float]
    y: Union[int, float]
    z: Union[int, float, None] = None


@dataclass
class TlBr:
    # tl: Point = Point(-1, -1)
    # br: Point = Point(-1, -1)
    tl: Point = field(default_factory=lambda: Point(-1, -1))
    br: Point = field(default_factory=lambda: Point(-1, -1))

    


class Labelling:
    def __init__(
        self, 
        dir_img, 
        dir_label,
        dir_deprecated,
        classes=None,
        window_width=800,
        window_height=600,
        window_name='usls inspect tools',
        trackerbar_img_name='IMAGES',
        trackerbar_class_name='CLASSES',
        with_QT=True
    ):

        # TODO: disable trackbar and overlap
        self.opencv_window_init_test()  # opencv windows init test
        self.with_QT = with_QT   # dont use qt, no trackbar, statusbar, overlay

        # windows 
        self.window_name = window_name
        self.window_width = window_width
        self.window_height = window_height

        # tracker bars
        self.trackerbar_img_name = trackerbar_img_name
        self.trackerbar_class_name = trackerbar_class_name

        # dirs
        self.dir_img = dir_img
        self.dir_label = dir_label if dir_label else self.dir_img

        # create output dir if not exist
        if not Path(self.dir_label).exists():
            Path(self.dir_label).mkdir()
        self.dir_deprecated = dir_deprecated

        CONSOLE.log(f"IMG   DIR: {Path(self.dir_img).resolve()}")
        CONSOLE.log(f"LABEL DIR: {Path(self.dir_label).resolve()}")
        

        self.mode = InspectMode.read    # new: mode

        self.HIDE_BBOX_LABEL = False  # hide label flag
        self.SINGLE_CLS_INDEX = None   # only show one specific class

        # bboxes blink
        self.DO_BLINKING = False
        self.BLINK_OR_NOT_SWITCHER = False

        # line thickness  &  line thickes adjust
        self.MIN_LINE_WIDTH = False  # min line width
        self.LINE_THICKNESS = 1            
        self.LINE_THICKNESS_ADJUST = False   # line thickness adjust flag

        # images
        self.IMG_IDX_CURRENT = 0         # 当前的img index
        self.IMG_CURRENT = None          # current image
        self.IMG_OBJECTS = list()            # 当前页面总所有bbox
        self.deprecated_img_set = set()       # 无法正常读取的image

        # classes
        self.CLS_IDX_CURRENT = 0         # current class index

        # bbox status
        self.PRVE_WAS_DOUBLE_CLICK = False   # previous left-button double click
        self.HAS_BBOX_SELECTED = False        # any bbox been selected
        self.SELECTED_BBOX_IDX = -1              # 选中后，IMG_OBJECTS中的第 idx 个

        # cursor 
        self.CURSOR = Point(0, 0)
        self.POINTS_DET = TlBr()

        self.CLASS_LIST = self.parse_label_classes(classes)  # parse label classes
        self.IMAGE_PATH_LIST = self.laod_image(self.dir_img)  # load all images path

        # img & class count
        self.IMG_COUNT = len(self.IMAGE_PATH_LIST) - 1  
        self.CLS_COUNT = len(self.CLASS_LIST) - 1

        # create window 
        # cv2.WINDOW_FREERATIO   cv2.WINDOW_KEEPRATIO, WINDOW_GUI_NORMAL, WINDOW_GUI_EXPANDED, cv2.WINDOW_NORMAL
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL) 
        cv2.resizeWindow(self.window_name, self.window_width, self.window_height)

        # mouse listen callback
        cv2.setMouseCallback(self.window_name, self.mouse_listener)

        # mode trackbar
        # trackerbar_mode_name = list(InspectMode.__members__.keys())
        # cv2.createTrackbar(str(trackerbar_mode_name) + '\n', self.window_name, 0, len(trackerbar_mode_name), lambda: None)
        
        # info
        if self.with_QT:
            cv2.createTrackbar('>>>><<<<<<>>>><<<>>', self.window_name, 0, 999, lambda x: None)


        # images trackbar
        if self.with_QT and self.IMG_COUNT != 0:
            cv2.createTrackbar(self.trackerbar_img_name, self.window_name, 0, self.IMG_COUNT, self.set_img_index)   


        # class trackbar
        if self.with_QT and self.CLS_COUNT != 0:
            self.trackerbar_class_name = self.trackerbar_class_name + '\n' + str(classes) + '\n'
            cv2.createTrackbar(self.trackerbar_class_name, self.window_name, 0, self.CLS_COUNT, self.set_class_index)


        self.set_img_index(0)  # initialize the img index=0  !! entrypoint set CLS_IDX_CURRENT
        self.COLOR_PALETTE = Palette(shuffle=False)    # colors palette
        CONSOLE.log(f"{HELP_MSG}")  # help message



    def mainloop(self):
        # main loop
        while True:
            color = self.COLOR_PALETTE(int(self.CLS_IDX_CURRENT), bgr=False)  # color for every class
            tmp_img = self.IMG_CURRENT.copy()    # clone the img   
            img_height_current, img_width_current = tmp_img.shape[:2]   # height, width

            # calculate line-thickness
            if self.MIN_LINE_WIDTH:
                self.LINE_THICKNESS = 1
            else:
                self.LINE_THICKNESS = max(round(sum(tmp_img.shape) / 2 * 0.003), 1) if not self.LINE_THICKNESS_ADJUST else self.LINE_THICKNESS      # line width

            # current class index and it's class name
            class_name = self.CLASS_LIST[self.CLS_IDX_CURRENT]
            
            # current image path, relative path: img/img_1.jpg
            img_path = self.IMAGE_PATH_LIST[self.IMG_IDX_CURRENT]
            label_path = Path(self.dir_label) / (Path(img_path).stem + '.txt')  # get corresponding label path
            
            if self.with_QT:
                # statusbar info
                status_msg = (
                    f"Mode: {self.mode}" + "\t" * 8 + 
                    f"CURSOR: ({self.CURSOR})" + "\t" * 8 + 
                    f"NUM_BBOXES: {str(len(self.IMG_OBJECTS))}" + "\t" * 8 +
                    f"IMG RESOLUTION: ({img_height_current}, {img_width_current})" + "\t" * 5 +
                    f"IMAGE PATH: {Path(img_path).name}"  + "\t" * 10 + 
                    f"LABEL PATH: {Path(label_path).name}"  + "\t" * 10
                )
                cv2.displayStatusBar(self.window_name, status_msg)
            
            # Blink bboxes
            # TODO: do_blinking()
            if self.DO_BLINKING:

                if self.BLINK_OR_NOT_SWITCHER == False:
                    tmp_img, self.IMG_OBJECTS = self.draw_bboxes_from_file(
                        img=tmp_img, 
                        label_path=label_path, 
                        color_palette=self.COLOR_PALETTE,   # Color type  
                        line_thickness=0,  # line_thickness = 0 
                        classes_list=self.CLASS_LIST,   # classes list
                        show_single_cls=self.SINGLE_CLS_INDEX,  # int or None 
                        hide_label=self.HIDE_BBOX_LABEL
                    )
                    self.BLINK_OR_NOT_SWITCHER = True   # ~
                else:
                    tmp_img, self.IMG_OBJECTS = self.draw_bboxes_from_file(
                        img=tmp_img, 
                        label_path=label_path, 
                        color_palette=self.COLOR_PALETTE,   # Color type  
                        line_thickness=self.LINE_THICKNESS,  # line_thickness
                        classes_list=self.CLASS_LIST,   # classes list
                        show_single_cls=self.SINGLE_CLS_INDEX,  # int or None 
                        hide_label=self.HIDE_BBOX_LABEL
                    )
                    self.BLINK_OR_NOT_SWITCHER = False   # ~
            else:
                # draw already done bounding boxes
                tmp_img, self.IMG_OBJECTS = self.draw_bboxes_from_file(
                    img=tmp_img, 
                    label_path=label_path, 
                    color_palette=self.COLOR_PALETTE,   # Color type  
                    line_thickness=self.LINE_THICKNESS,  # line_thickness
                    classes_list=self.CLASS_LIST,   # classes list
                    show_single_cls=self.SINGLE_CLS_INDEX,  # int or None 
                    hide_label=self.HIDE_BBOX_LABEL
                )


            # detection labelling
            if self.mode == InspectMode.mark_dets:
                # TODO: do_mark_dets()

                # show cursor line for drawing
                cv2.line(tmp_img, (self.CURSOR.x, 0), (self.CURSOR.x, img_height_current), color, self.LINE_THICKNESS)
                cv2.line(tmp_img, (0, self.CURSOR.y), (img_width_current, self.CURSOR.y), color, self.LINE_THICKNESS)

                # show label or not when drawing
                if not self.HIDE_BBOX_LABEL:
                    self.show_objects_labels(
                        img=tmp_img,
                        label=class_name,
                        line_thickness=self.LINE_THICKNESS,
                        x=self.CURSOR.x,
                        y=self.CURSOR.y,                       
                        color=color,
                    )

                # --------------------------
                #  hightlight selected bbox
                # --------------------------
                if self.HAS_BBOX_SELECTED:

                    # hight-light seletec bbox
                    ind, x1, y1, x2, y2 = self.IMG_OBJECTS[self.SELECTED_BBOX_IDX]  # selected bbox
                    mask_highlight = np.zeros((tmp_img.shape), dtype=np.uint8)
                    _lw = self.LINE_THICKNESS // 2   # border
                    cv2.rectangle(
                        mask_highlight, 
                        (x1 - _lw, y1 - _lw),
                        (x2 + _lw, y2 + _lw), 
                        (255, 255, 255, 0), 
                        -1, 
                        cv2.LINE_AA
                    )
                    tmp_img = cv2.addWeighted(tmp_img, 1, mask_highlight, 0.5, 0)

                    
                # --------------------------
                #   draw with rect
                # --------------------------

                # detection draw with 2 points
                if self.POINTS_DET.tl.x != -1:   # 1st point
                    # draw partial bbox 
                    cv2.rectangle(
                        tmp_img, 
                        (self.POINTS_DET.tl.x, self.POINTS_DET.tl.y),
                        (self.CURSOR.x, self.CURSOR.y), 
                        color, 
                        self.LINE_THICKNESS
                    )

                    # second click: bottom_right point
                    if self.POINTS_DET.br.x != -1:
                        # save bbox right after get point_2  =>  label.txt
                        line = self.idxyxy2idcxcywh(
                            cls_idx=self.CLS_IDX_CURRENT, 
                            det_points=self.POINTS_DET, 
                            img_w=img_width_current, 
                            img_h=img_height_current
                        ) # (x,y,x,y) => (x,y,w,h)

                        # save label file, txt
                        with open(label_path, 'a') as f:
                            if os.path.getsize(label_path) == 0:
                                f.write(line)
                            else:
                                f_r = open(label_path, "r").read()   # read a
                                if f_r[-1] == '\n':
                                    msg = line
                                else:
                                    msg = '\n' + line
                                f.write(msg)
                        
                        # reset
                        self.POINTS_DET = TlBr()


            # other labellling
            elif self.mode == InspectMode.mark_kpts:
                pass
            elif self.mode == InspectMode.doodle:
                pass

            
            cv2.imshow(self.window_name, tmp_img)  # current show
            self.keys_listener(label_path=label_path, delay=1)   # opencv key listening

            # if window gets closed then quit
            if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

        cv2.destroyAllWindows()


        # deal with wrong img: can not be opened by opencv
        if len(self.deprecated_img_set) > 0:
            CONSOLE.log(f"Warning: {len(self.deprecated_img_set)} images can not be read by OpenCV")
            
            # create dir
            self.dir_deprecated = smart_path(Path(self.dir_deprecated), exist_ok=False, sep='-')  # increment run
            self.dir_deprecated.mkdir(parents=True, exist_ok=True)  # make dir for every page

            # move
            for img in tqdm(self.deprecated_img_set, desc='moving deprecated...'):
                shutil.move(img, str(self.dir_deprecated))


    def show_objects_labels(
            self,
            *,
            img,
            label,
            line_thickness,
            x,
            y,
            color,
            font=cv2.FONT_HERSHEY_SIMPLEX,
            lineType=cv2.LINE_AA
        ):
        # show objects labels when loaded from files and cursor line

        text_w, text_h = cv2.getTextSize(
            label,   # label
            0,
            fontScale=line_thickness / 3, 
            thickness=max(line_thickness - 1, 1)
        )[0]  # get text width, height

        # check if label is outside of image
        outside = y - text_h - 3 >= 0  
        cv2.putText(
            img, 
            label, 
            (x, y - 2 if outside else y + text_h + 3), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            line_thickness / 3, 
            color, 
            thickness=int(line_thickness * 0.7), 
            lineType=cv2.LINE_AA
        )

        return img



    def laod_image(self, directory):
        # load images path

        images_path_sorted = sorted(
            [str(x) for x in Path(directory).iterdir() if x.suffix.lower() in IMG_FORMAT],
            key=natural_sort
        )
        if len(images_path_sorted) == 0:
            raise ValueError(f'Empty image directory: {directory}.')
        return images_path_sorted


    def parse_label_classes(self, args: List):
        # label class parser
        # TODO: yaml file support
        classes_list = list()
        if len(args) == 1 and args[0].endswith('.txt'):    # txt file
            with open(args[0]) as f:
                for line in f:
                    classes_list.append(line.strip())
        else:   # args classes 
            classes_list = args
        return classes_list



    def set_class_index(self, x):
        # set current class index

        self.CLS_IDX_CURRENT = x


    def set_img_index(self, x):
        # set current img index & set current image & check image
        # TODO
        
        self.IMG_IDX_CURRENT = x   # set current image index
        p = self.IMAGE_PATH_LIST[self.IMG_IDX_CURRENT]  # set current image  
     
        # opencv read img
        self.IMG_CURRENT = cv2.imread(p)
        if self.IMG_CURRENT is None:
            self.IMG_CURRENT = np.ones((800, 800, 3))  # create a empty img
            # show notification
            cv2.putText(
                self.IMG_CURRENT, 
                "Deprecated image!\nor Image no longer exists.", 
                (10, self.IMG_CURRENT.shape[0]//2), 
                cv2.FONT_HERSHEY_SIMPLEX,
                1, 
                (0,0,0), 
                thickness=2, 
                lineType=cv2.LINE_AA
            )

            # save wrong images path, delete all these image at the end of the program
            self.deprecated_img_set.add(p)



    def idxyxy2idcxcywh(
            self, 
            *,
            cls_idx, 
            det_points: TlBr, 
            img_w, 
            img_h, 
            eps=1e-8
        ):
        # idxyxy -> idcxcywh

        # boundary check and rectify
        det_points.tl.x = min(max(eps, det_points.tl.x), img_w - eps) 
        det_points.br.x = min(max(eps, det_points.br.x), img_w - eps) 
        det_points.tl.y = min(max(eps, det_points.tl.y), img_h - eps) 
        det_points.br.y = min(max(eps, det_points.br.y), img_h - eps)

        # check again
        # if (det_points.tl.x >= det_points.br.x) or (det_points.tl.y >= det_points.br.y):
        #     raise ValueError(f'point of bottom-right {det_points.br} should greater than point of top-left {det_points.tl}')

        # convert
        cx = float((det_points.tl.x + det_points.br.x) / (2.0 * img_w) )
        cy = float((det_points.tl.y + det_points.br.y) / (2.0 * img_h))
        w = float(abs(det_points.br.x - det_points.tl.x)) / img_w
        h = float(abs(det_points.br.y - det_points.tl.y)) / img_h

        # double check of boundary
        if not all([0 <= x <= 1 for x in [cx, cy, w, h]]):
            CONSOLE.log(f"Wrong coordination -> cx: {cx}, cy: {cy}, w: {w}, h: {h}.")
            sys.exit()
            

        items = map(str, [cls_idx, cx, cy, w, h])
        return ' '.join(items)



    def draw_bboxes_from_file(
            self, 
            *,
            img, 
            label_path, 
            color_palette,   # Color type  
            line_thickness,  # line_thickness
            classes_list,   # classes list
            show_single_cls=None,  # int or None 
            hide_label=False
        ):
        # read label.txt and draw all bboxes
        
        height, width = img.shape[:2]   # h, w
        objects_idxyxy = list()   # all objects per image

        # Drawing bounding boxes from the files
        if Path(label_path).is_file():
            with open(label_path) as f:   # read label file, .txt default  # TODO: kpts
                for idx, line in enumerate(f):

                    cls_id, cx, cy, box_w, box_h, *kpts_list = line.split()
                    box_w, box_h, cx, cy = map(float, (box_w, box_h, cx, cy))  # to float
                    cls_id = int(cls_id)   # to int
                    cls_name = classes_list[cls_id]  # class name

                    # xyxy
                    xmin = int(width * cx - width * box_w / 2.0)   # tl
                    xmax = int(width * cx + width * box_w / 2.0)   
                    ymin = int(height * cy - height * box_h / 2.0)
                    ymax = int(height * cy + height * box_h / 2.0)

                    # show single class
                    if show_single_cls is not None:   
                        if cls_id != show_single_cls:
                            continue    
                    objects_idxyxy.append([cls_id, xmin, ymin, xmax, ymax])   # update objects

                    # draw bbox
                    color = color_palette(cls_id, bgr=False)   # color palette
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, line_thickness, cv2.LINE_AA)  

                    # Display Label if has label txt
                    if not hide_label:
                        self.show_objects_labels(
                            img=img,
                            label=cls_name,
                            line_thickness=line_thickness,
                            x=xmin,
                            y=ymin,
                            color=color,
                        )
        return img, objects_idxyxy




    def set_selected_bbox(
            self, 
            set_cls_trackbar=True
        ):
        # left double click in bbox => select the smallest bbox, and set that bbox
        # mark self.SELECTED_BBOX_IDX --> id
        # mark self.HAS_BBOX_SELECTED true
        # set class_trackbar_position

        # smallest bbox flag
        smallest_area = -1

        # if clicked inside multiple bboxes selects the smallest one
        for idx, obj in enumerate(self.IMG_OBJECTS):
            ind, x1, y1, x2, y2 = obj

            # line width (consider) 
            # margin = 2 * self.LINE_THICKNESS
            # x1 = x1 - margin  
            # y1 = y1 - margin
            # x2 = x2 + margin
            # y2 = y2 + margin
            
            # check if mouse_xy is in bbox
            if x1 <= self.CURSOR.x <= x2 and y1 <= self.CURSOR.y <= y2:   
                self.HAS_BBOX_SELECTED = True     # set bbox selected
                tmp_area = abs(x2 - x1) * abs(y2 - y1)  # area of bbox

                if tmp_area < smallest_area or smallest_area == -1:
                    smallest_area = tmp_area
                    self.SELECTED_BBOX_IDX = idx   # set selected bbox index

                    # set class trackbar position
                    if set_cls_trackbar: 
                        cv2.setTrackbarPos(self.trackerbar_class_name, self.window_name, ind)    
            



    def edit_selected_bbox(
            self, 
            *,
            idxyxy_selectd,
            action: Dict
        ):

        # supported action: delete & change_class_id   

        # get label file (.txt)
        p_label = Path(self.dir_label) / (Path(self.IMAGE_PATH_LIST[self.IMG_IDX_CURRENT]).stem + '.txt')

        # load original label file
        with open(p_label, 'r') as f_original:
            lines_original = f_original.readlines()

        # find out modified objects index
        for idx, idxyxy in enumerate(self.IMG_OBJECTS):
            if idxyxy == idxyxy_selectd:
                idx_modified = idx
                break

        # re-write label file
        with open(p_label, 'w') as f:
            for idx, line in enumerate(lines_original):
                if idx != idx_modified:   # nothing changed
                    f.write(line)
                elif 'change_class_id' in action.keys():   # change class idx
                    new_label_line = str(action['change_class_id']) + line[1:]
                    f.write(new_label_line)
                elif 'delete' in action.keys():    # delete
                    continue
                else:
                    pass



    def mouse_listener(self, event, x, y, flags, param):
        # mouse callbacks

        # -------------------------
        #   mark_dets mode
        # -------------------------
        if self.mode == InspectMode.mark_dets:
            if event == cv2.EVENT_MOUSEMOVE:
                self.CURSOR.x = x
                self.CURSOR.y = y

            # left button double click -> select object
            elif event == cv2.EVENT_LBUTTONDBLCLK:
                self.PRVE_WAS_DOUBLE_CLICK = True    
                self.POINTS_DET.tl = Point(-1, -1)   # reset top_left point

                # if clicked inside a bounding box we set that bbox
                self.set_selected_bbox(set_cls_trackbar=True)

            # right button pressed down
            elif event == cv2.EVENT_RBUTTONDOWN:  #     EVENT_RBUTTONUP 
                self.set_selected_bbox(set_cls_trackbar=False)   # cancel set class
                if self.HAS_BBOX_SELECTED:   # delete box when box is selected
                    # deal with selected bbox
                    self.edit_selected_bbox(
                            idxyxy_selectd=self.IMG_OBJECTS[self.SELECTED_BBOX_IDX], 
                            action={'delete': None}
                        )
                    self.HAS_BBOX_SELECTED = False    # mark false when box is deleted

            # left button pressed down
            elif event == cv2.EVENT_LBUTTONDOWN:
                if self.PRVE_WAS_DOUBLE_CLICK:  # cancel last double click
                    self.PRVE_WAS_DOUBLE_CLICK = False
                else:  # Normal left click
                    if self.POINTS_DET.tl.x == -1:  # in bbox ---> set select
                        if self.HAS_BBOX_SELECTED:  # selected  -> de-selected
                            self.HAS_BBOX_SELECTED = False
                        else:  # first click
                            self.POINTS_DET.tl = Point(x, y)  # top-left point
                    else:  # second click
                        _threshold = 5  # minimal size for bounding box to avoid errors
                        if abs(x - self.POINTS_DET.tl.x) > _threshold or abs(y - self.POINTS_DET.tl.y) > _threshold:
                            self.POINTS_DET.br = Point(x, y)    # bottom-right point
        
        # -------------------------
        #   doodle mode
        # -------------------------            
        elif self.mode == InspectMode.doodle:
            pass



    def opencv_window_init_test(self):
        # init window with overlap
        try:
            cv2.namedWindow('Test')   
            cv2.displayOverlay('Test', 'Test overlap', 10)  
            cv2.displayStatusBar('Test', 'Test status bar', 10)
        except cv2.error as e:
            CONSOLE.log(f"Exception: {e}")
        cv2.destroyAllWindows()   



    def keys_listener(self, label_path, delay=1):
        # ---------------- Key Listeners ------------------------
        pressed_key = cv2.waitKey(delay)

        # h/H -> help 
        if pressed_key in (ord('h'), ord('H')):
            if self.with_QT:
                cv2.displayOverlay(self.window_name, HELP_MSG, 1000)


        # ---------------------------------------
        # a,d -> images [previous, next]
        # ---------------------------------------
        elif pressed_key in (ord('a'), ord('A'), ord('d'), ord('D')):

            if not self.HAS_BBOX_SELECTED:

                # show previous image
                if pressed_key in (ord('a'), ord('A')):     
                    self.IMG_IDX_CURRENT = 0 if self.IMG_IDX_CURRENT - 1 < 0 else self.IMG_IDX_CURRENT - 1

                # show next image index
                elif pressed_key in (ord('d'), ord('D')):
                    self.IMG_IDX_CURRENT = self.IMG_COUNT if self.IMG_IDX_CURRENT + 1 > self.IMG_COUNT else self.IMG_IDX_CURRENT + 1

                # set current img index and show corresponding image
                self.set_img_index(self.IMG_IDX_CURRENT)


                if self.with_QT:
                    cv2.setTrackbarPos(self.trackerbar_img_name, self.window_name, self.IMG_IDX_CURRENT)  # update img trackbar 
                
                # set the adjust flag False
                self.LINE_THICKNESS_ADJUST = False    

        

        # ---------------------------------------
        # w,s -> class  [previous, next]
        # ---------------------------------------
        elif pressed_key in (ord('s'), ord('S'), ord('w'), ord('W')):

            # set current class index
            # next class
            if pressed_key in (ord('s'), ord('S')):
                self.CLS_IDX_CURRENT = self.CLS_COUNT if self.CLS_IDX_CURRENT - 1 < 0 else self.CLS_IDX_CURRENT - 1

            # last class
            elif pressed_key in (ord('w'), ord('W')):
                self.CLS_IDX_CURRENT = 0 if self.CLS_IDX_CURRENT + 1 > self.CLS_COUNT else self.CLS_IDX_CURRENT + 1

            if self.with_QT:
                # update class trackbar                
                cv2.setTrackbarPos(self.trackerbar_class_name, self.window_name, self.CLS_IDX_CURRENT)

            # when select, use W/S to edit bbox's class
            if self.HAS_BBOX_SELECTED:

                # deal with selected bbox
                self.edit_selected_bbox(
                    idxyxy_selectd=self.IMG_OBJECTS[self.SELECTED_BBOX_IDX], 
                    action={'change_class_id': self.CLS_IDX_CURRENT}
                )

        # ---------------------------------------
        # n/N => hide label
        # ---------------------------------------
        elif pressed_key in (ord('n'), ord('N')):
            self.HIDE_BBOX_LABEL = not self.HIDE_BBOX_LABEL

            if self.with_QT:
                cv2.displayOverlay(self.window_name, 'Press n to hide Label or show Label.', 800)

        # ---------------------------------------
        # '+-' => adjust line thickness
        # ---------------------------------------
        elif pressed_key in (ord('='), ord('+')):

            # set the adjust flag TRUE
            self.LINE_THICKNESS_ADJUST = True
            
            # get the max line width
            max_t = max(round(sum(self.IMG_CURRENT.shape) / 2 * 0.003), 2) + 5

            # increate the line width
            if self.LINE_THICKNESS <= max_t:
                self.LINE_THICKNESS += 1
                if self.with_QT:
                    cv2.displayOverlay(self.window_name, f'Line Thickness +1, now = {self.LINE_THICKNESS}', 800)
            else:
                if self.with_QT:
                    cv2.displayOverlay(self.window_name, 'Line Thickness has reach the max value!', 800)

        elif pressed_key in (ord('-'), ord('_')):
            self.LINE_THICKNESS_ADJUST = True
            min_t = 1
            if self.LINE_THICKNESS > min_t:
                self.LINE_THICKNESS -= 1
                if self.with_QT:
                    cv2.displayOverlay(self.window_name, f'Line Thickness -1, now = {self.LINE_THICKNESS}', 800)
            else: 
                if self.with_QT:
                    cv2.displayOverlay(self.window_name, 'Line Thickness has reach the min value!', 800)

        # ---------------------------------------
        # i/I => display the info in this img(size, path, num_bboxes)
        # ---------------------------------------
        # elif pressed_key in (ord('i'), ord('I')):



        # ---------------------------------------
        # b/b => blink bboxes in current img
        # ---------------------------------------
        elif pressed_key in (ord('b'), ord('B')):
            self.DO_BLINKING = not self.DO_BLINKING


        # ---------------------------------------
        # c/C  =>  Remove all bboxes in this img, 
        # specifically, delete the annotation file(.txt)
        # ---------------------------------------
        elif pressed_key in (ord('c'), ord('C')):
            if not self.HAS_BBOX_SELECTED:
                if self.with_QT:
                    cv2.displayOverlay(self.window_name, f"Clean bbox one by one! rest num = {len(self.IMG_OBJECTS)}", 800)
                
                if Path(label_path).exists():
                    Path(label_path).unlink()
                else:
                    if self.with_QT:
                        cv2.displayOverlay(self.window_name, f"No bboxes in this img!", 800)

        # -----------------------------------------------------
        # r/R  =>  switch mode between mark_dets and read
        # -----------------------------------------------------
        elif pressed_key in (ord('r'), ord('R')):
            if self.with_QT:
                cv2.displayOverlay(self.window_name, f"Switch mode between READ and MARK", 800)
            
            if self.mode == InspectMode.read:
                self.mode = InspectMode.mark_dets
            elif self.mode == InspectMode.mark_dets:
                self.mode = InspectMode.read



        # ---------------------------------------
        # l/L  =>  shuffle bbox color
        # ---------------------------------------
        elif pressed_key in (ord('l'), ord('L')):
            self.COLOR_PALETTE = Palette(shuffle=True)

            if self.with_QT:
                cv2.displayOverlay(self.window_name, f"Palette palette shuffled!", 800)


        # ---------------------------------------
        # t/T  =>  min line width
        # ---------------------------------------
        elif pressed_key in (ord('t'), ord('T')):
            self.MIN_LINE_WIDTH = not self.MIN_LINE_WIDTH


        # ---------------------------------------
        # 0-8 -> select to show single class
        # 9 -> show all
        # ---------------------------------------
        elif pressed_key in range(48, 57):  # 0-8 => 48-56
            value = int(chr(pressed_key))
            if value <= self.CLS_COUNT:
                self.SINGLE_CLS_INDEX = value
                if self.with_QT:
                    cv2.displayOverlay(self.window_name, f"Only show class: {self.SINGLE_CLS_INDEX} => {self.CLASS_LIST[self.SINGLE_CLS_INDEX]}", 1000)
            else:
                self.SINGLE_CLS_INDEX = None
                
                if self.with_QT:
                    cv2.displayOverlay(
                        self.window_name, 
                        f"No class: {value}, Max class is {self.CLS_COUNT} => {self.CLASS_LIST[self.CLS_COUNT]}. Show All bboxes",
                        1000
                    )


        elif pressed_key == 57:  # 9
            self.SINGLE_CLS_INDEX = None


        # -----------------------------
        # ESC -> quit key listener
        # -----------------------------
        # elif pressed_key == 27:
            # break
        # ---------------- Key Listeners END ------------------------





def run_inspect(args: DictConfig):

    labelling = Labelling(
        dir_img=args.img_dir, 
        dir_label=args.label_dir if args.label_dir else args.img_dir,
        dir_deprecated=args.depreacated_dir,
        classes=args.classes,
        window_width=args.window_width,
        window_height=args.window_height,
        window_name='usls labelling',
        trackerbar_img_name='IMAGES',
        trackerbar_class_name='CLASSES',
        with_QT=not args.no_qt 
    )
    with CONSOLE.status("[bold cyan]Doing inspect...") as status:
        labelling.mainloop()
