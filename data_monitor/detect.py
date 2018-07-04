
import time
import datetime
import serial
import sys
import logging
from threading import Lock


from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


thread = None
thread_lock = Lock()


def detect(name, num, t):
    ser.write('{},{},{}'.format(name, num, t).encode())
    read_val = ''
    while True:
        read_val = ser.readline().decode().replace("\r\n", "")
        if read_val != 'over':
            yield read_val
        else:
            break


def background_thread():
    ser.write('sound,1,9999'.encode())
    ser.readline()
    data, t = [], []
    while True:
        read_val = ser.readline().decode().replace("\r\n", "")
        data.append(read_val)
        t.append(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f')[:-2])
        if len(data) == 150:
            socketio.sleep(0.001)
            print(data)
            socketio.emit('server_response',
                          {'sound': data, 'time': t},
                          namespace='/test')
            data, t = [], []
        # t = time.strftime('%M:%S', time.localtime())


def background_thread2():
    ser.write('all,1,8888'.encode())
    sound, light1, s_t, l_t1 = [], [], [], []
    while True:
        try:
            read_val = ser.readline().decode()
            if read_val.replace('\r\n', '').isdigit():
                sound.append(read_val.replace('\r\n', ''))
                s_t.append(datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S.%f')[:-2])
            for line in read_val.split('\r\n'):
                ct = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if ',' in line:
                    for k, v in enumerate(line.split(',')):
                        if v.isdigit():
                            light1.append(v)
                            l_t1.append(ct + '.' + str(k))
                elif ';' in line:
                    for d in line.split(';'):
                        print(d)
                elif '|' in line:
                    for k, v in enumerate(line.split('|')):
                        if v.isdigit():
                            sound.append(v)
                            s_t.append(ct + '.' + str(k))

            if len(sound) == 150:
                print(sound)
                socketio.sleep(0.001)
                socketio.emit('server_response',
                              {'led1': light1, 'sound': sound, 'time': s_t},
                              namespace='/test')
                sound, light1, s_t, l_t1 = [], [], [], []
        except Exception as e:
            print(e)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    port = 'COM8'
    baudrate = '115200'
    try:
        ser = serial.Serial(port=port, baudrate=baudrate)
        ser.timeout = 1
        time.sleep(2)
    except Exception as e:
        logging.log(logging.ERROR, 'Cannot open port[{}]: {}'.format(port, e))
        sys.exit()
    socketio.run(app, debug=False)
