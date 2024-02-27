import shutil

import pandas
import glob
import os
from tqdm import tqdm

oldpath = r"C:\Users\zhuangzexuan\Documents\proj_python\BDD2yolo\dawn_dusk\labels"
imagespath = r"C:\Users\zhuangzexuan\Documents\proj_python\Mydata\val\images"
filenamedir = glob.glob(oldpath+"\*.txt")
newpath = r"C:\Users\zhuangzexuan\Documents\proj_python\BDD2yolo\dawn_dusk\images"

def label2image(filepath):
    filelist = filepath.split("\\")
    name = filelist[-1].replace("txt","jpg")
    image = imagespath+'\\'+name
    return image

for i in tqdm(filenamedir):
    image = label2image(i)
    shutil.copy(image,newpath)
