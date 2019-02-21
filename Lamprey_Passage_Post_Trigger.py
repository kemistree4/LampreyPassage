import io
import random
import picamera
import RPi.GPIO as GPIO
import datetime 
import logging

def write_video(stream):
    print('Writing video!')
    with stream.lock:
        # Find the first header frame in the video
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        # Write the rest of the stream to disk
        with io.open('motion.h264', 'wb') as output:
            output.write(stream.read())

# Variables
BEAM_PIN = 4                                # Pin we are using to read the IR break beam switch
LED_PIN = 17                                # Pin we are using to activate the LED

# Setup the GPIO
GPIO.setmode(GPIO.BCM)                 # GPIO layout mode      
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup the gpio pin we are reading from as a pullup input
GPIO.setup(LED_PIN, GPIO.OUT)

with picamera.PiCamera() as camera:
    stream = picamera.PiCameraCircularIO(camera, seconds=30)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(1)
            if input != 1:
                #define time format for filenames and log output
                now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
                timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S") #Variable to update name of video files with current date and time
                GPIO.output(17,GPIO.HIGH) #Turns on indicator light
                camera.wait_recording(30)
                write_video(stream)
                GPIO.output(17,GPIO.LOW) #Turns off indicator light
                time.sleep(0.05) #Debounce wait
    finally:
        camera.stop_recording()
