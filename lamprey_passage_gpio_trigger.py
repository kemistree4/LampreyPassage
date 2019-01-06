# Imports
from picamera import PiCamera
import time
import RPi.GPIO as GPIO

# Variables
camera = PiCamera()
PIN = 4                                # Pin we are using to read the IR break beam switch
prev_input = 0             # Variable to track if trigger beam is broken
now = time.localtime(time.time())
# Setup the GPIO
GPIO.setmode(GPIO.BCM)          # GPIO layout mode      
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup the gpio pin we are reading from as a pullup input

# Loop checking the switch
while True:
    # Read the switch value
    input = GPIO.input(PIN)

    # If the last reading was low and this one high, record for 30 secs
    if not input == 1:
        print(time.asctime(now))
        print('Lamprey Detected')
        camera.start_recording('/media/pi/Lexar/test_video/video.h264')
        time.sleep(30)
        camera.stop_recording()
                    
    # Wait slightly for debounce
    time.sleep(0.05)

#send an email to my work email with time of detection
    
#code also needs to:
  #send an email to my work email with time of detection (beam is broken)
  #make log file of all detections
  #continue recording if beam is broken past initial 30 secs
  #save videos to a USB drive
