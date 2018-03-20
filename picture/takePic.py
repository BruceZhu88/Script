# -*- coding: utf-8 -*-
'''
Created on 2017/4/21/

@author: Tester Bruce Zhu
'''

import cv2
import time
import os

def makeDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def take_pic(num,interval,filePath,fileName):#num:number of pictures you need to take, interval:interval time
    # initialize the camera
    window_name='camera'
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cam = cv2.VideoCapture(0)   # 0,1 -> index of camera, choose correct one
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,1920)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,1080)
    for i in range(num):
        s, img = cam.read()
        if s:    # frame captured without any errors
            cv2.imshow("camera",img)
            #cv2.waitKey(0)
            makeDir(filePath)
            filename = "%s\\%s_%s.jpg" % (filePath,fileName,i)
            cv2.imwrite(filename,img) #save image
            time.sleep(interval)#set capture interval time
            cv2.waitKey(1)
    cam.release()
    cv2.destroyWindow("camera")


if __name__ == '__main__':

    take_pic(2,0.2,"./capture/results","results")
    #take_pic(10,0.3,"./capture/wakeUp","wakeUp")

