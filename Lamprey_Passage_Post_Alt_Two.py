#Imports
import io
import time
import picamera
import RPi.GPIO as GPIO
import logging
import datetime
import random

#Variables
BEAM_PIN = 4
LED_PIN = 17

#Setup the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

def write_video(stream):
    print('Writing video!')
    with stream.lock:
        # Find the first header frame in the video
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        # Write the rest of the stream to disk
        with io.open('/media/pi/Lexar/test_video/{}.h264'.format(timestamp), 'wb') as output:
            output.write(stream.read())

with picamera.PiCamera() as camera:
    stream = picamera.PiCameraCircularIO(camera, seconds=20)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(0.25)
            input = GPIO.input(Beam_PIN)
            if input != 1:
                GPIO.output(17,GPIO.HIGH)
                # Keep recording for 10 seconds and only then write the
                # stream to disk
                camera.wait_recording(10)
                #define time format for filenames and log output
                now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
                timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S") #Variable to update name of video files with current date and time
                write_video(stream)
    finally:
        camera.stop_recording()
        GPIO.output(17,GPIO.LOW)
