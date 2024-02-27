import os
import glob
import shutil
from tqdm import tqdm
oldpath = r"C:\Users\zhuangzexuan\Documents\proj_python\bdd100k_labels\bdd100k\labels\100k\val"
newpath = r"C:\Users\zhuangzexuan\Documents\proj_python\BDD2yolo\dawn_dusk\labels"
filedir = glob.glob(oldpath+"\*.txt")

for i in tqdm(filedir):
    shutil.move(i,newpath)
