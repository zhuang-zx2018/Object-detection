#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright @ 2022 zhuangzexuan <895440769@qq.com>
import glob
import re
import os
import json
from tqdm import tqdm
import shutil


def search_file(data_dir, pattern=r'\.jpg$'):
    root_dir = os.path.abspath(data_dir)
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if re.search(pattern, f, re.I):
                abs_path = os.path.join(root, f)
                # print('new file %s' % absfn)
                yield abs_path


class Bdd2yolov5:
    def __init__(self):
        self.bdd100k_width = 1280
        self.bdd100k_height = 720
        self.select_categorys = ["person", "car", "bus", "truck", "bike", "motor"]
        self.cat2id = {
            "person": 0,
            "car": 1,
            "bus": 1,
            "truck": 1,
            "bike": 1,
            "motor": 1
        }

    @property
    def all_categorys(self):
        return ["person", "rider", "car", "bus", "truck", "bike",
                "motor", "traffic light", "traffic sign", "train"]

    def _filter_by_attr(self, weather, attr=None):
        if attr is None:
            return False
            # 过滤掉晚上的图片
        # if attr['timeofday'] in ['daytime','night']:
        #     return True
        if attr['weather'] == weather:
            return False
        else:
            return True

    def _filter_by_box(self, w, h):
        # size ratio
        # 过滤到过于小的小目标
        threshold = 0.001
        if float(w * h) / (self.bdd100k_width * self.bdd100k_height) < threshold:
            return True
        return False

    def bdd2yolov5(self, path, weather):
        lines = ""
        with open(path) as fp:
            j = json.load(fp)
            if self._filter_by_attr(weather, j['attributes']):
                return
            for fr in j["frames"]:
                dw = 1.0 / self.bdd100k_width
                dh = 1.0 / self.bdd100k_height
                for obj in fr["objects"]:
                    if obj["category"] in self.select_categorys:
                        idx = self.cat2id[obj["category"]]
                        cx = (obj["box2d"]["x1"] + obj["box2d"]["x2"]) / 2.0
                        cy = (obj["box2d"]["y1"] + obj["box2d"]["y2"]) / 2.0
                        w = obj["box2d"]["x2"] - obj["box2d"]["x1"]
                        h = obj["box2d"]["y2"] - obj["box2d"]["y1"]
                        if w <= 0 or h <= 0:
                            continue
                        if self._filter_by_box(w, h):
                            continue
                        # 根据图片尺寸进行归一化
                        cx, cy, w, h = cx * dw, cy * dh, w * dw, h * dh
                        line = f"{idx} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n"
                        lines += line
                if len(lines) != 0:
                    # 转换后的以*.txt结尾的标注文件我就直接和*.json放一具目录了
                    # yolov5中用到的时候稍微挪一下就行了
                    yolo_txt = path.replace(".json", ".txt")
                    with open(yolo_txt, 'w') as fp2:
                        fp2.writelines(lines)
                # print("%s has been dealt!" % path)


def movetxt(oldpath, newpath):
    filedir = glob.glob(oldpath + "\*.txt")
    for i in tqdm(filedir):
        shutil.move(i, newpath)
    return


def mkdir(path, weather):
    weatherdir = path + "\\" + weather
    os.mkdir(weatherdir)
    os.mkdir(weatherdir + "\\" + "images")
    os.mkdir(weatherdir + "\\" + "labels")
    return


def label2image(filepath, images_path):
    filelist = filepath.split("\\")
    name = filelist[-1].replace("txt", "jpg")
    image = images_path + '\\' + name
    return image


def move_images(new_label_path, images_path, new_image_path):
    filenamedir = glob.glob(new_label_path + "\*.txt")
    for i in tqdm(filenamedir):
        image = label2image(i, images_path)
        shutil.copy(image, new_image_path)
    return


if __name__ == "__main__":
    bdd_label_dir = r"C:\Users\zhuangzexuan\Documents\proj_python\bdd100k_labels\bdd100k\labels\100k\val"
    images_path = r"C:\Users\zhuangzexuan\Documents\proj_python\Mydata\val\images"
    ROOT = r"C:\Users\zhuangzexuan\Documents\proj_python\BDD2yolo"
    cvt = Bdd2yolov5()
    weatherlist = ["clear", "partly cloudy", "snowy", "rainy", "overcast"]
    for weather in tqdm(weatherlist):
        for path in search_file(bdd_label_dir, r"\.json$"):
            cvt.bdd2yolov5(path, weather)
        mkdir(ROOT, weather)
        new_label_path = r"C:\Users\zhuangzexuan\Documents\proj_python\BDD2yolo\{0}\labels".format(weather)
        movetxt(bdd_label_dir, new_label_path)
        new_image_path = r"C:\Users\zhuangzexuan\Documents\proj_python\BDD2yolo\{0}\images".format(weather)
        move_images(new_label_path, images_path, new_image_path)
