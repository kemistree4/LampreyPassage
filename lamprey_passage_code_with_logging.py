# Imports
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import datetime 
import logging
import schedule

# Variables
camera = PiCamera()
BEAM_PIN = 4                                # Pin we are using to read the IR break beam switch
log_time = datetime.datetime.now().strftime('%m%d%y')
#create logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG) # log all escalated at and above DEBUG

# Setup the GPIO
GPIO.setmode(GPIO.BCM)                 # GPIO layout mode      
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup the gpio pin we are reading from as a pullup input

# Loop checking the switch
while True:
    # Read the switch value
    input = GPIO.input(BEAM_PIN)

    # If the GPIO reading goes from high to low, record for 30 secs
    if input != 1:
        #define time format for filenames and log output
        now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
        timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S") #Variable to update name of video files with current date and time
        #add a file handler
        hdlr = logging.FileHandler('/media/pi/F8AF-129D/log_files/{}.log'.format(log_time))
        # create a formatter and set the formatter for the handler
        formatter = logging.Formatter('%(asctime)s %(message)s')
        hdlr.setFormatter(formatter)
        #add the handler to the logger
        logger.addHandler(hdlr)
        logger.info('Lamprey Detected!')
        logger.removeHandler(hdlr)
        camera.start_recording('/media/pi/F8AF-129D/videos/{}.h264'.format(timestamp)) #Recording video file to Lexar thumb drive
        camera.wait_recording(30)
        camera.stop_recording()
        time.sleep(0.05) #Debounce wait
        
def test_video():
    now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
    timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S")
    camera.start_recording('/media/pi/F8AF-129D/test_videos/{}.h264'.format(timestamp)) #Recording video file to Lexar thumb drive
    camera.wait_recording(15)
    camera.stop_recording()
    time.sleep(0.5)
    return

#Makes a test video everyday at 6 am and saves it to the test_video folder.
schedule.every().day.at("06:00").do(test_video,"Time for the 6 am test video")


