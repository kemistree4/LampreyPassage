# Imports
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import datetime 

# Variables
camera = PiCamera()
PIN = 4                                # Pin we are using to read the IR break beam switch
prev_input = 0                         # Variable to track if trigger beam is broken
now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out

# Setup the GPIO
GPIO.setmode(GPIO.BCM)                 # GPIO layout mode      
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup the gpio pin we are reading from as a pullup input

# Loop checking the switch
while True:
    # Read the switch value
    input = GPIO.input(PIN)

    # If the GPIO reading goes from high to low, record for 30 secs
    if input != 1:
        timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S") #Variable to update name of video files with current date and time
        print(time.asctime(now))
        camera.start_recording('/media/pi/Lexar/test_video/{}.h264'.format(timestamp)) #Recording video file to Lexar thumb drive
        camera.wait_recording(30)
        camera.stop_recording()
        
    #Debounce wait
    time.sleep(0.05)            

#code also needs to:
  #send an email to my work email with time of detection (beam is broken)
  #make log file of all detections
  #continue recording if beam is broken past initial 30 secs

