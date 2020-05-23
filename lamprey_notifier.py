#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 22:41:03 2020

@author: rikeem
"""

import smtplib
import time
from datetime import datetime
import os
from datetime import timedelta
import sys

#Trigger count variables
today_count = 0
yesterday_count = 0

# General Email Parameters 
username = 'warmspringslaps1' #you don't need the "@gmail.com" bit.
password = 'zdzp lfld uykt ndgm' #Had to turn on allowances for less security apps, two factor authentication, and generate an app passoword for this to work
From = "warmspringslaps1@gmail.com"
To =  "rikeem_sholes@fws.gov, rikeem.sholes@gmail.com"


def email(condition = "start"):
    print("Attempting to send email")
    seperator = "\r\n"
    Subject_notifier = "Daily Trap Update"
    Body_notifier = "Yesterday you had " + str(yesterday_count) + " trigger(s). So far today you have " + str(today_count) + " trigger(s)."
    if condition == 'start':        
        Body = seperator.join((
            "From: %s" % From,
            "To: %s" % To,
            "Subject: %s" % Subject_notifier,
            "",
            Body_notifier,
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
    
video_files = os.listdir("/media/rikeem/C659-66D9/Videos")     
today_timestamp = datetime.now().strftime("%m%d%y")
yesterday_timestamp = (datetime.now() - timedelta(1)).strftime('%m%d%y')


for file in video_files:
    date_slice = file[0:6]
    if date_slice == today_timestamp:
        today_count = today_count + 1
    elif date_slice == yesterday_timestamp:
        yesterday_count = yesterday_count + 1
    else:
        continue
 
email('start')
sys.exit()