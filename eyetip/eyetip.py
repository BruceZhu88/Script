# -*- coding: utf-8 -*-
from time import sleep
import sys

if sys.version < '3':
    from Tkinter import *
else:
    from tkinter import *


def showMessage(t):
    # show reminder message window
    root = Tk()
    root.withdraw()  # hide window
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight() - 100
    root.resizable(False, False)

    root.title("Warning!!")
    frame = Frame(root, relief=RIDGE, borderwidth=3)
    frame.pack(fill=BOTH, expand=1)
    label = Label(frame, text="You have been working {} minutes! Please have a break!!".format(t),
                  font="Monotype\ Corsiva -20 bold")
    label.pack(fill=BOTH, expand=1)
    button = Button(frame, text="OK", font="Cooper -25 bold",
                    fg="red", command=root.destroy)
    button.pack(side=BOTTOM)

    root.update_idletasks()
    root.attributes('-topmost', 1)  # this is for always on top position
    root.deiconify()  # now the window size was calculated
    root.withdraw()  # hide the window again 防止窗口出现被拖动的感觉 具体原理未知?
    root.geometry('%dx%d+%d+%d' % (root.winfo_width() + 10, root.winfo_height() + 10,
                                   (screenwidth - root.winfo_width())/2, (screenheight - root.winfo_height())/2))
    root.deiconify()
    root.mainloop()


while True:
    mydelaymin = input('Input time(M): ')
    if mydelaymin.isnumeric():
        mydelaymin = float(mydelaymin)
        print('Start counting ...')
        break
    else:
        print('Please input digit number!')

while True:
    sleep(mydelaymin * 60)  # 参数为秒
    showMessage(mydelaymin)
