from utils import CenterlineExtraction,imgPad,concat,connect
import numpy as np
import cv2
import json
import time
import os
import json
from math import log10
import numpy as np
from osgeo import ogr, gdal
from tqdm import tqdm
if __name__ == '__main__':
    tic = time.time()
    dataset = gdal.Open("lushan_65556_mask.tif")
    width = dataset.RasterXSize  # 图像宽度
    height = dataset.RasterYSize  # 图像高度
    img = dataset.ReadAsArray(0, 0, width, height) #.transpose((1,2,0))
    toc = time.time()
    print("读取tif耗时：",toc-tic)
    # img = cv2.imread("lushan_65556_mask.tif", -1)
    print(img.shape)
    padSize=1024
    pad=100
    oriSize=padSize-(pad*2)
    json_list=[]
    for i in tqdm(range(0,64506,oriSize)): #y
        for j in range(0,64506,oriSize): #x
            tmp=imgPad((j,i),img,(oriSize,oriSize),pad)
            res=CenterlineExtraction(tmp, 0, 0,(j-pad,i-pad))
            tmp_json={}
            tmp_json["x"]=j
            tmp_json["y"]=i
            tmp_json["data"]=res
            json_list.append(tmp_json)
            # filename="./output/"+"{}_{}_{}.json".format(j,i,pad)
            # with open(filename,'w') as file_obj:
                # json.dump(res,file_obj)
    geojson = concat(json_list)
    
    exclude=[]
    new_js=geojson.copy()
    for index,feature in enumerate(new_js["features"]):
        if(feature["pop"]>0):
            continue
        new_js["features"][index]["pop"]=1
        connect(new_js,index)
    index=0
    while(True):
        if(new_js["features"][index]["pop"]==2):
            new_js["features"].pop(index)
        else:
            index+=1
        if(len(new_js["features"])==index):
            break
    filename="connect.json"
    print("end")
    toc = time.time()
    print("总耗时：",toc-tic)
    with open(filename,'w') as file_obj:
        json.dump(new_js,file_obj)

    #print(res)