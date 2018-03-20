# -*- coding: utf-8 -*-
'''
Created on 2017/4/21/

@author: Tester Bruce Zhu
'''

import math, operator
from PIL import Image
from takePic import *

def compare_pic(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    h1 = image1.histogram()
    h2 = image2.histogram()
    rms = math.sqrt(reduce(operator.add,
            map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    rms=int (rms)
    return rms

def compare(pic1, pic2, num):
    num_matched = 0
    for i in range(num):
        results = r"%s\results_%s.jpg"%(pic1,i)
        rms = compare_pic(results, pic2)
        if rms < 15000:
            num_matched += 1
            print "results_%s  rms: %s"%(i,rms)
    if num_matched>0:
        print "Ratio of match: %s/%s"%(num_matched, num)
        return True
    else:
        print "No one could be matched!"
        return False

