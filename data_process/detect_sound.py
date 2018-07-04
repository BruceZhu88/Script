

import time
import sys
import datetime
import serial


ser = serial.Serial("COM7")
ser.timeout = 1
time.sleep(2)  # here must add sleep >= 2, will be cannot receive if not
print('Start running?(y/n):')
if input().lower() != 'y':
    print('Exit')
    ser.close()
    sys.exit()

with open('./data/LED.txt', 'w') as f:
    f.write("")
with open('./data/LED.txt', 'a') as f:
    f.write("#title: CA17 LED(Wifi) brightness[]\n")


#ser.write('relay,4,200'.encode())
start = time.time()
ser.write('light,1,20'.encode())
time.sleep(0.2)
while time.time() - start < 19:
    read_val = ser.readline().decode().replace("\r\n", "")
    value = datetime.datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S.%f')[:-3] + ": " + read_val
    print(value)
    with open('./data/LED.txt', 'a') as f:
        f.write(value + "\n")

print('Done!')
'''
while True:
    ser.write('light'.encode())
    time.sleep(0.01)
    read_val = ser.readline().decode().replace("\r\n", "")
    value = datetime.datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S.%f')[:-3] + ": " + read_val
    print(value)
    with open('./data/LED.txt', 'a') as f:
        f.write(value + "\n")
'''
# s = ser.l_serial.read()
# print(ord(s))

ser.close()
