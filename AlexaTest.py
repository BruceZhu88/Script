# -*- coding: utf-8 -*-
'''
Created on 2017/4/21/

@author: Tester Bruce Zhu
'''
#import winsound
import threading
import pygame
from picCompare import *
global play, audioPath


def tym_print(str):
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    print "%s %s"%(currentTime,str)
    
def sleep(i):
    tym_print("sleep %s"%i)
    time.sleep(i)    

def playAudio(path):
    #winsound.PlaySound(path, winsound.SND_FILENAME)
    pygame.mixer.init(frequency=15500, size=-16, channels=4)
    track = pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops=0, start=0.0)
    
class Thread_PlayAudio(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = "Thread-PlayAudio")
        self.thread_stop = False
    
    def run(self):
        global play,audioPath
        while not self.thread_stop:
            if play==True:
                playAudio(audioPath)
                play = False

    def stop(self): 
        self.thread_stop = True            

if __name__ == '__main__':
    wakeUp = r".\capture\wakeUp\wakeUp_0.jpg"
    standby = r".\capture\standby\standby_0.jpg"
    results = r".\capture\results"
    
    play = False
    audioPath = ".\music\Alexa_3.wav"
    threadPlayAudio = Thread_PlayAudio()
    threadPlayAudio.start()
    
    for i in range(3):
        tym_print("---------------------------This is the %d times"%(i+1))
        tym_print("Start to play audio %s"%audioPath)
        play = True
        tym_print("Start to take picture")
        take_pic(60,0.1,"./capture/results","results")
        compare(results, wakeUp, 60)
        sleep(10)
