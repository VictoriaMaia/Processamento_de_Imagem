import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d


def callback_func(x):
   t = cv2.getTrackbarPos('threshold','thresh')

   ret,im_thresh1 = cv2.threshold(im,t,255,cv2.THRESH_BINARY)
#   im_thresh1= cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
#                                cv2.THRESH_BINARY, t, -2)
   cv2.imshow('thresh',im_thresh1)
   return

def acharThreshol(im):
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.namedWindow('thresh',cv2.WINDOW_NORMAL)

#     im = cv2.imread(sys.argv[1],0)

    width = im.shape[1]
    height = im.shape[0]

    cv2.createTrackbar('threshold','thresh',0,255,callback_func)
    cv2.imshow('image',im)

    while(1):
        k = cv2.waitKey(0) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()



