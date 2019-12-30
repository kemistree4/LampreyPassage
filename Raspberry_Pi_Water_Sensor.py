#!/usr/bin/python

# About 

# This script uses a Raspberry Pi to sense for the presense or absense of water. 
# If there is water, an email is sent and a light comes on.
# When it's dry again, another email is sent, and the light turns off.

# Gmail login credentials to send email

username = 'warmspringslaps1' #you don't need the "@gmail.com" bit.
password = 'zdzp lfld uykt ndgm' #Had to turn on allowances for less security apps, two factor authentication, and generate an app passoword for this to work

# General Email Parameters 

From = "warmspringslaps1@gmail.com"
To =  "rikeem_sholes@fws.gov"

# Email Parameters when sensor is Wet 

Subject_wet = "RPi Water Sensor is WET"
Body_wet = "Your water sensor is wet."

# Email Parameters when semsor is Dry 

Subject_dry = "RPi Water Sensor is DRY"
Body_dry = " Your water sensor is dry again!"

import smtplib
import RPi.GPIO as GPIO
import string
import time

# Function Definitions

#takes either "wet" or "dry" as the condition.
def email(condition):
    print("Attempting to send email")
    seperator = "\r\n"
    if condition == 'wet':
        Body = seperator.join((
        "From: %s" % From,
        "To: %s" % To,
        "Subject: %s" % Subject_wet,
        "",
        Body_wet,
        ),)
    if condition == 'dry':        
        Body = seperator.join((
            "From: %s" % From,
            "To: %s" % To,
            "Subject: %s" % Subject_dry,
            "",
            Body_dry,
            ),)
    
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    print("Logging in...")
    server.login(username,password)
    print("Logged in as "+username+".")
    server.sendmail(From, [To], Body)
    server.quit()
    print("Email sent.")

#Tests whether water is present.
# returns 0 for dry
# returns 1 for wet
# tested to work on pin 18 
def RCtime (RCpin):
    reading = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1) 
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while True:
        if (GPIO.input(RCpin) == GPIO.LOW):
            reading += 1
        if reading >= 1000:
            return 0
        if (GPIO.input(RCpin) != GPIO.LOW):
            return 1

# Turns on the indicator light 
# tested to work on pin 17
def light_on (pin):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# Turns off the indicator light
# tested to work on pin 17
def light_off(pin):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Main Loop

print('Waiting for wetness...')
while True:
    time.sleep(1) # check for wetness every second
    if RCtime(18) == 0:
        light_off(17)
        print("Sensor is wet")
        email('wet')
        print("Waiting for dryness...")
        while True:
            time.sleep(1) # check for dryness every second
            if RCtime(18) == 1:
                light_on(17)
                print("Sensor is dry again")
                email('dry')
                print("Waiting for wetness...")
                break
