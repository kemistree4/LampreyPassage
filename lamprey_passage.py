# Imports
import picamera
import sys
import time
import RPi.GPIO as GPIO
import os
import json
import tinys3
import requests
from time import gmtime, strftime

# Variables
PIN = 4                                # Pin we are using to read the door switch
prev_input = 0             # Variable to track if trigger beam is broken

# Setup the GPIO
GPIO.setmode(GPIO.BCM)          # GPIO layout mode      
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup the gpio pin we are reading from as an input
# Loop checking the switch
while True:
  # Read the switch value
  input = GPIO.input(PIN)

  # If the last reading was low and this one high, record for 30 secs
  if ((not prev_input) and input):
    print (time)

    raspivid -o video.h264 -t 30000
    
    # may also use?:
    #camera.start_recording('home/pi/video.h264)
    #sleep(30)
    #camera.stop_recording
    
  # Update previous input
  prev_input = input
  # Wait slightly for debounce
  time.sleep(0.05)

#code also needs"
  #send an email to my work email with time of detection (beam is broken)
  #make log file of all detections
  #continue recording if beam is broken past initial 30 secs
  #save videos to a USB drive