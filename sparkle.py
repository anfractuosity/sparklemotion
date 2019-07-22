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

VIDS = "vids"

WAIT = 30 # time to wait before / after motion

prior_image = None

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

        if np.count_nonzero(r) > 0 and np.mean(r[np.nonzero(r)]) > 3.0 and (r > 3.0).sum() > 100 :
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
    camera.resolution = (1920, 1080)

    stream = picamera.PiCameraCircularIO(camera, seconds=10)
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
                stream.copy_to(os.path.join(VIDS,'%d.h264' % (idv-WAIT)), seconds=WAIT)
                stream.clear()

                while detect_motion(camera):
                    camera.wait_recording(WAIT,splitter_port=1)

                print('Motion stopped!')
                idv += 1

                camera.split_recording(stream,splitter_port=1)
    finally:
        camera.stop_recording()

