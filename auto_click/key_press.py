
import _thread
import keyboard
import mouse
import time
import pyscreenshot as ImageGrab
from find_obj import *


def detect_key():
    while True:
        k = keyboard.read_key()
        print(k)
        if 'down up' in k:
            print('down')
        elif 'up up' in k:
            print('up')


def print_pressed_keys(e):
    line = ', '.join(str(code) for code in keyboard._pressed_events)
    # '\r' and end='' overwrites the previous line.
    # ' '*40 prints 40 spaces at the end to ensure the previous line is cleared.
    print(line)
    if '72' in line:
        print('up')
    elif '75' in line:
        print('left')
    elif '77' in line:
        print('right')
    elif '29' in line:
        print('Ctrl')
    elif '42' in line:
        print('Shift')
    elif '56' in line and '47' in line:
        print('Alt + v')
    # print('\r' + line + ' '*40, end='')


def mouse_click(obj_pic):
    src_pic = './pic/screenshot.png'
    im = ImageGrab.grab()
    im.save('./pic/screenshot.png')
    try:
        pos = coordinate(src_pic, obj_pic)
        mouse.move(pos[0], pos[1])
        mouse.click(button='left')
        return True
    except Exception as e:
        return False


def wait_click(obj):
    while True:
        if mouse_click(obj):
            break
        time.sleep(2)
keyboard.hook(print_pressed_keys)
keyboard.wait()
# up 72
# left 75
# right 77
# Ctrl 29
# Shift 42

# detect_key()
    # keyboard.press_and_release('up')

'''
if __name__ == "__main__":
    # fullscreen
    wait_click('./pic/nox.png')
    wait_click('./pic/icon_neteasy.png')
    wait_click('./pic/neteasy_me.png')

    # wait_click('./pic/neteasy_signing.png')
    for j in range(2):
        wait_click('./pic/neteasy_sign.png')
        for i in range(10):
            print(i)
            if mouse_click('./pic/neteasy_viewAds.png'):
                break
            if mouse_click('./pic/neteasy_iKnow.png'):
                wait_click('./pic/neteasy_sign.png')
                wait_click('./pic/neteasy_viewAds.png')
                break
            time.sleep(2 + i)
        time.sleep(20)
        for i in range(10):
            if mouse_click('./pic/neteasy_closeAds.png'):
                break
            time.sleep(2 + i)
'''