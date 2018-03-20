
import keyboard
import pyttsx3
import clipboard


def print_pressed_keys(e):
    line = ', '.join(str(code) for code in keyboard._pressed_events)
    # '\r' and end='' overwrites the previous line.
    # ' '*40 prints 40 spaces at the end to ensure the previous line is cleared.
    # print(line)
    '''
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
    '''
    if '91' in line and '46' in line:
        # print('Win + c')
        txt = clipboard.paste()
        if txt != '':
            txt = txt.replace('\r\n', ' ')
            txt = txt.replace('\n', ' ')
            tts(txt)
    # print('\r' + line + ' '*40, end='')


def tts(txt):
    engine = pyttsx3.init()
    engine.say(txt)
    engine.setProperty('rate', 100)
    engine.runAndWait()


keyboard.hook(print_pressed_keys)
keyboard.wait()
