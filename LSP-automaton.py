import matplotlib.pyplot as plt
from PIL import Image
from pylab import *
import numpy as np
import os
import tensorflow as tf
import keras
from keras.utils import to_categorical
import _thread
import keyboard
from shutil import copyfile

global tag
global lst
global net
global tot
tag=1
lst=[]
net=tf.keras.models.load_model('ST_recognizer_model.h5')
tot=0

class Data(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y

def listdir(path,L):
    for file in os.listdir(path):
        if tag==0:
            return
        try:
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                flag=0
                listdir(file_path, L)
            elif os.path.splitext(file_path)[1]=='.jpeg':
                L.append(file_path)
            elif os.path.splitext(file_path)[1]=='.jpg':
                L.append(file_path)
            elif os.path.splitext(file_path)[1]=='.png':
                L.append(file_path)
            elif os.path.splitext(file_path)[1]=='.bmp':
                L.append(file_path)
        except:
            pass

def PngArray(img):
    pre=array(img)
    #print(pre.dtype)
    re=np.zeros(64*64*3)
    re=re.reshape([64,64,3])
    for i in range(64):
        for j in range(64):
            #print(i,j)
            re[i][j][0],re[i][j][1],re[i][j][2]=pre[i][j][0],pre[i][j][1],pre[i][j][2]
    return re

def Recognize(img):
    img64=img.resize((64,64))
    #plt.imshow(img64)
    #plt.show()
    data=np.zeros(64*64*3,dtype=int)
    data=data.reshape([1,64,64,3])
    data[0]=PngArray(img64)
    #print(data.shape)
    predict=net.predict(data[:1])
    #print("debug: "+str(predict.shape))
    if(predict[0][1]>predict[0][0]):
        return True
    return False

def Run():
    global tot
    ptr=-1
    while True:
        try:
            if size(lst)-1>ptr:
                ptr+=1
                try:
                    path=lst[ptr]
                    print("Recognizing: "+path,end="\r")
                    img=Image.open(path)
                    if(Recognize(img)):
                        tot+=1
                        copyfile(path,"art\\"+str(tot)+os.path.splitext(path)[1])
                        print("Good! "+path)
                except:
                    pass
        except:
            pass

def init():
    try:
        os.makedirs("art")
    except:
        pass
    
if __name__=='__main__':
    init()
    root=input("Input the root:")
    _thread.start_new_thread(listdir,(root,lst))
    _thread.start_new_thread(Run,())
    while True:
        try:
            if keyboard.is_pressed('j'):
                tag=0
                break
        except:
            pass
