import ctypes
import json
from ctypes import *
import cv2
import numpy as np
import os
import json
from math import log10
from platform import system
from tqdm import tqdm
#加载DLL
if system() == 'Windows':
    pDLL = WinDLL("./centerline.dll",winmode=0)
elif system()=='Linux':
    pDLL = cdll.LoadLibrary("./libMySharedLib.so")
pDLL.CenterlineExtraction.restype=ctypes.c_uint
pDLL.CenterlineExtraction.argtypes=[ctypes.POINTER(ctypes.c_ubyte),c_int,c_int,c_int,c_int,ctypes.POINTER(ctypes.POINTER(c_float)),ctypes.POINTER(ctypes.POINTER(c_float)),ctypes.POINTER(ctypes.POINTER(c_uint))]
# print(pDLL)
def CenterlineExtraction(img,pruned,smooth,offset=(0,0)):
    offsetX,offsetY=offset
    ox=pointer(c_float(0.))
    oy=pointer(c_float(0.))
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
            f['coordinates'].append([ox[pi]+offsetX,oy[pi]+offsetY])
            cv2.circle(img,(int(ox[pi]),int(oy[pi])),1,20)
        data['features'].append(f)
    return data
    filename='test.json'

def imgPad(startPoint,img,size,pad):
    height,width=size
    x,y=startPoint
    tmp=np.zeros((pad*2+height,pad*2+width))
    # print("tmp shape:",tmp.shape)
    # print("x,y:",x,y," img shape:",img[y:y+height,x:x+width].shape)
    tmp[pad:pad+height+pad,pad:pad+width+pad]=img[y:y+height+pad,x:x+width+pad]
    if(y!=0):
        tmp[:pad,pad:]=img[y-pad:y,x:x+width+pad]
    if(x!=0):
        tmp[pad:,:pad]=img[y:y+height+pad,x-pad:x]
    if(x!=0 and y!=0):
        tmp[:pad,:pad]=img[y-pad:y,x-pad:x]
    return tmp
    
def concat(json_list):
    geojson={}
    geojson["type"]="FeatureCollection"
    geojson["features"]=[]
    total_num=0
    line_id=0
    for json_tmp in json_list: 
        tmp = json_tmp["data"]
        # print(tmp)
        start_x,start_y=json_tmp["x"],json_tmp["y"]
        start_x=int(start_x)
        start_y=int(start_y)
        for js in tmp["features"]:
            f={}
            f["pop"]=0 # 0有链接 1无连接 2预备删除 
            f["start"]={}
            x=start_x//824
            y=start_y//824
            zero_num=10**len(str(y))
            f["start"]["xy"]= [x*zero_num+(y)]
            f["start"]["connect"]=[]
            f["type"]="Feature"
            f["properties"]={}
            f["properties"]["FID"]=0
            f["geometry"]={}
            f["geometry"]["type"]="LineString"
            tmp_list=np.array(js["coordinates"])
            total_num+=tmp_list.shape[0]
            a1=(tmp_list[:,0]>=start_x)   
            if(False in a1):
                f["start"]["connect"].append((x-1)*zero_num+y)
            a2=(tmp_list[:,0]<=start_x+824)
            if(False in a2):
                f["start"]["connect"].append((x+1)*zero_num+y)
            b1=tmp_list[:,1]>=start_y
            zero_num=10**len(str(y-1))
            if(False in b1):
                f["start"]["connect"].append(x*zero_num+y-1)
            b2=tmp_list[:,1]<=start_y+824
            zero_num=10**len(str(y+1))
            if(False in b2):
                f["start"]["connect"].append(x*zero_num+y+1)
            selection=a1*a2*b1*b2
            if(False not in selection):
                f["pop"]=1
            tmp_list=tmp_list[a1*a2*b1*b2,:]
            tmp_list[:,0]=115.806+(tmp_list[:,0]*0.000002682)
            tmp_list[:,1]=29.6047-(tmp_list[:,1]*0.000002682)
            f["geometry"]["coordinates"]=tmp_list.tolist()
            if(len(f["geometry"]["coordinates"])==0):
                continue
            geojson["features"].append(f)
    return geojson
    
def findLineIndex(myjs,cnn_index):
    line_index=[]
    for index,feature in enumerate(myjs["features"]):
        if(feature["pop"]>0):
            continue
        if(cnn_index in feature["start"]["xy"]):
            line_index.append(index)
    return line_index

from math import sqrt
def calDis(point1,point2):
    dis=sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    return dis
def checkConn(line1,line2,th=5):
    if(len(line1)==0 or len(line2)==0): return []
    head1=line1[0]
    bottom1=line1[-1]
    head2=line2[0]
    bottom2=line2[-1]
    if(calDis(head1,head2)<th):
        line1.reverse()
        return line1+line2
    if(calDis(head1,bottom2)<th):
        line1.reverse()
        line2.reverse()
        return line1+line2
    if(calDis(bottom1,head2)<th): 
        return line1+line2
    if(calDis(bottom1,bottom2)<th): 
        line2.reverse()
        return line1+line2
    return []

def connect(myjs,index):
    new_cnn_list=[]
    for cnn_index in myjs["features"][index]["start"]["connect"]:
        line_list=findLineIndex(myjs,cnn_index)
        for line_index in line_list:
            tmp=checkConn(myjs["features"][index]["geometry"]["coordinates"],myjs["features"][line_index]["geometry"]["coordinates"])
            if(len(tmp)==0):
                continue
            myjs["features"][index]["geometry"]["coordinates"]=tmp
            myjs["features"][index]["start"]["xy"]+=myjs["features"][line_index]["start"]["xy"]
            new_cnn_list=new_cnn_list+myjs["features"][line_index]["start"]["connect"]
            myjs["features"][line_index]["pop"]=2
    myjs["features"][index]["start"]["connect"]=new_cnn_list
    if(len(new_cnn_list)==0):
        return 0
    connect(myjs,index)

