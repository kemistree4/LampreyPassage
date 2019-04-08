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
log_time = datetime.datetime.now().strftime('%m%d%y')
#create logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG) # log all escalated at and above DEBUG

# Setup the GPIO
GPIO.setmode(GPIO.BCM)                 # GPIO layout mode      
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup the gpio pin we are reading from as a pullup input
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(21, GPIO.IN)

# Loop checking the switch
while True:
    # Read the switch value
    input = GPIO.input(21)

    # If the GPIO reading goes from high to low, record for 30 secs
    if input == 1:
        #define time format for filenames and log output
        time.sleep(5)
        now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
        timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S") #Variable to update name of video files with current date and time
        GPIO.output(17,GPIO.HIGH) #Starts light
        #add a file handler
        hdlr = logging.FileHandler('/media/pi/CC45-36E0/log_files/{}.log'.format(log_time))
        # create a formatter and set the formatter for the handler
        formatter = logging.Formatter('%(asctime)s %(message)s')
        hdlr.setFormatter(formatter)
        #add the handler to the logger
        logger.addHandler(hdlr)
        logger.info('Lamprey Detected!')
        logger.removeHandler(hdlr)
        camera.resolution = (1024, 768)
        camera.framerate = 40
        time.sleep(1)
        camera.start_recording('/media/pi/CC45-36E0/videos/{}.h264'.format(timestamp)) #Recording video file to Lexar thumb drive
        camera.wait_recording(30)
        camera.stop_recording()
        GPIO.output(17,GPIO.LOW) #Turns off light
        time.sleep(0.05) #Debounce wait
