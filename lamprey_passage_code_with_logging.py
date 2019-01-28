# Imports
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import datetime 
import logging

# Variables
camera = PiCamera()
BEAM_PIN = 4                                # Pin we are using to read the IR break beam switch
LED_PIN = 17                                # Pin we are using to activate the LED

# Setup the GPIO
GPIO.setmode(GPIO.BCM)                 # GPIO layout mode      
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup the gpio pin we are reading from as a pullup input
GPIO.setup(LED_PIN, GPIO.OUT)

# Loop checking the switch
while True:
    # Read the switch value
    input = GPIO.input(BEAM_PIN)

    # If the GPIO reading goes from high to low, record for 30 secs
    if input != 1:
        now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
        timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S") #Variable to update name of video files with current date and time
        log_time = datetime.datetime.now().strftime('%m%y')
        logger = logging.getLogger('myapp')
        hdlr = logging.FileHandler('/media/pi/Lexar/log/{}.log'.format(log_time))
        formatter = logging.Formatter('%(asctime)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.error('Lamprey Detected!')
        logger.info('Lamprey Detected!')
        GPIO.output(17,GPIO.HIGH)
        print(time.asctime(now))
        camera.start_recording('/media/pi/Lexar/test_video/{}.h264'.format(timestamp)) #Recording video file to Lexar thumb drive
        camera.wait_recording(30)
        camera.stop_recording()
        GPIO.output(17,GPIO.LOW)
        time.sleep(0.05) #Debounce wait

#code also needs to:
  #send an email to my work email with time of detection (beam is broken)
  #make log file of all detections
  #continue recording if beam is broken past initial 30 secs
