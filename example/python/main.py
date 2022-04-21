from utils import CenterlineExtraction,imgPad
import numpy as np
import cv2
import json
import time
import json
from math import log10
from osgeo import ogr, gdal
if __name__ == '__main__':
    tic = time.time()
    dataset = gdal.Open("lushan_65556_mask.tif")
    width = dataset.RasterXSize  # 图像宽度
    height = dataset.RasterYSize  # 图像高度
    img = dataset.ReadAsArray(0, 0, width, height) #.transpose((1,2,0))
    # img = cv2.imread("lushan_65556_mask.tif", -1)
    print(img.shape)
    padSize=1024
    pad=100
    oriSize=padSize-(pad*2)
    for i in range(0,64506,oriSize): #y
        for j in range(0,64506,oriSize): #x
            tmp=imgPad((j,i),img,(oriSize,oriSize),pad)
            res=CenterlineExtraction(tmp, 0, 0,(j-pad,i-pad))
            filename="./output/"+"{}_{}_{}.json".format(j,i,pad)
            with open(filename,'w') as file_obj:
                json.dump(res,file_obj)
    # for i in range(2048,12288,4096): #y
    #     for j in range(2048,40960,4096): #x
    #         tmp=imgPad((j,i),img,(4096,4096),pad)
    #         res=CenterlineExtraction(tmp, 0, 0,(j-pad,i-pad))
    #         filename="./output/"+"{}_{}_{}.json".format(j,i,pad)
    #         with open(filename,'w') as file_obj:
    #             json.dump(res,file_obj)
    print("end")
    toc = time.time()
    print("耗时：",toc-tic)
    #print(res)