#!/usr/bin/python3

import socket
import threading
import sys
import os
import numpy as np
import io
import random
import picamera
import picamera.array
from picamera import mmal 
import datetime
import ctypes as ct
import toml

config = toml.load(open('config.toml'))
VIDS = config['videos']['path']
WAIT = 30 # time to wait before / after motion
motionv = False

def stream_service():

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 10000))
    server_socket.listen(0) 
    
    while True:
        try:
            conn = server_socket.accept()[0].makefile('wb')
            camera.start_recording(conn,splitter_port=3,format='h264')
            while True:
                camera.wait_recording(1,splitter_port=3)
        except Exception as e:
            try:
                camera.stop_recording(splitter_port=3)
            except:
                ok = 1
            continue

class MotionAnalyser(picamera.array.PiMotionAnalysis):

    def analyse(self, a):

        global motionv

        # Calculate the motion vector polar lengths
        r = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)

        #if np.count_nonzero(r) > 0 :
        #    print(np.mean(r[np.nonzero(r)]) ,  (r > 0.0).sum())

        if np.count_nonzero(r) > 0 and np.mean(r[np.nonzero(r)]) > config['motion']['mean_threshold'] and (r > 0.0).sum() > config['motion']['vector_threshold']:
            motionv = True
        else:
            motionv = False

def detect_motion(camera):
    global motionv
    print(motionv)
    return motionv

with picamera.PiCamera() as camera:

    print("Starting camera...")
    
    out = MotionAnalyser(camera) 
    #camera.awb_mode = 'greyworld'

    camera.hflip = config['camera']['hflip']
    camera.vflip = config['camera']['vflip']
    camera.resolution = (config['camera']['width'], config['camera']['height'])

    stream = picamera.PiCameraCircularIO(camera, seconds=WAIT)
    camera.framerate = 30
    camera.start_recording(stream, splitter_port=1,format='h264')
    camera.start_recording('/dev/null', splitter_port=2, format='h264', motion_output=MotionAnalyser(camera)) 

    t = threading.Thread(name='stream_service', target=stream_service)
    t.start()

    idv = 0

    try:
        while True:

            camera.wait_recording(1)

            if detect_motion(camera):

                print('Motion detected!')

                idv = datetime.datetime.now().timestamp()
                camera.split_recording(os.path.join(VIDS,'%d.h264' % idv),splitter_port=1)      

                stream.copy_to(os.path.join(VIDS,'%d.h264' % (idv-WAIT)), seconds=WAIT) # copy time before motion
                stream.clear()
                
                camera.wait_recording(WAIT,splitter_port=1)

                while detect_motion(camera):
                    camera.wait_recording(WAIT,splitter_port=1)

                print('Motion stopped!')

                idv += 1
                camera.split_recording(stream,splitter_port=1)
    finally:
        camera.stop_recording()

