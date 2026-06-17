#！/usr/bin/env python3

import os
import numpy as np
import cv2
from PIL import Image
from gurobipy import *

folder_name = 'demos/demo_01'
path = os.path.abspath(os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(__file__))))
path = os.path.join(path, folder_name)
size = cv2.imread(path+'/0.png').shape[1::-1]

imgs_list = []
files = os.listdir(path)
num = len(files)
print('Snapshot num: %s' %num)

videoWrite = cv2.VideoWriter(filename=path+'/video_3.mp4', 
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 
            fps=10, frameSize=size, isColor=True)

per  = 0
itr = 3000
print('Generate video from %s to %s.' %(per, per+itr))
for n in range(per, per+itr):
    img = cv2.imread(path+'/%s.png' %n)
    # print(n)
    if img is None:
        print('Error: there is no snapshot %s.png!' %n)
        continue
    imgs_list.append(img)

print(len(imgs_list))
for i in range(len(imgs_list)):
    videoWrite.write(imgs_list[i])
print('Finished')
videoWrite.release()
print('The video has been generated completely!')