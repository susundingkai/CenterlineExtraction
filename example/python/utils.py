import ctypes
import json
from ctypes import *
import cv2
import numpy as np
import os
from platform import system
def CenterlineExtraction(img,pruned,smooth):
    #加载DLL
    if system() == 'Windows':
        pDLL = WinDLL("./centerline.dll",winmode=0)
    elif system()=='Linux':
        pDLL = cdll.LoadLibrary("./libMySharedLib.so")
    pDLL.CenterlineExtraction.restype=ctypes.c_uint
    pDLL.CenterlineExtraction.argtypes=[ctypes.POINTER(ctypes.c_ubyte),c_int,c_int,c_int,c_int,ctypes.POINTER(ctypes.POINTER(c_float)),ctypes.POINTER(ctypes.POINTER(c_float)),ctypes.POINTER(ctypes.POINTER(c_uint))]
    print(pDLL)
    ox=pointer(c_float(0))
    oy=pointer(c_float(0))
    oi=pointer(c_uint(0))
    width=c_int(img.shape[1])
    height=c_int(img.shape[0])
    pruned=c_int(pruned)
    smooth=c_int(smooth)
    # img=cv2.imread("4.png",-1)
    img=np.array(img,dtype=np.uint8)[:,:]
    img_p=img.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    #调用动态链接库函数
    nsegs = pDLL.CenterlineExtraction(img_p,width,height,pruned,smooth,pointer(ox),pointer(oy),pointer(oi))
    data={}
    data['features']=[]
    for i in range(nsegs):
        f={}
        f['id']=i
        f['coordinates']=[]
        ssize=int(oi[i + 1]) - int(oi[i])
        for pi in range(int(oi[i]),int(oi[i+1])):
            f['coordinates'].append([ox[pi],oy[pi]])
            cv2.circle(img,(int(ox[pi]),int(oy[pi])),1,20)
        data['features'].append(f)
    return data
    filename='test.json'


