import smtplib
import time
from datetime import datetime
import os
from datetime import timedelta
import sys
from email.mime.text import MIMEText

try:
    import httplib
except:
    import http.client as httplib
    
def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False
    
#Trigger count variables
today_count = 0
yesterday_count = 0

# General Email Parameters 
username = 'warmspringslaps1' #you don't need the "@gmail.com" bit.
password = "qfeq uwac swuu ufrt" #'zdzp lfld uykt ndgm' #Had to turn on allowances for less security apps, two factor authentication, and generate an app passoword for this to work
From = "warmspringslaps1@gmail.com"
recipients = ["rwbiz@msn.com", (Insert other emails here)]
To =  ", ".join(recipients)

def email(condition = "start"):
    print("Attempting to send email")
    seperator = "\r\n"
    Subject_notifier = "Daily Trap Update"
    Body_notifier = "This is your daily report for Eel Lake lamprey monitor. Yesterday you had " + str(yesterday_count) + " trigger(s). So far today you have " + str(today_count) + " trigger(s)."
    if condition == 'start':
        msg = MIMEText(Body_notifier)
        msg['Subject'] = Subject_notifier
        msg['From'] = From
        msg['To'] = To
    
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    print("Logging in...")
    server.login(username,password)
    print("Logged in as "+username+".")
    server.sendmail(From, recipients, msg.as_string())
    server.quit()
    print("Email sent.")
    
video_files = os.listdir("/media/pi/F8AF-129D2/videos")     
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
if have_internet() == True:
    email(condition = "start")
    sys.exit()
else:
    sys.exit()
    
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
if have_internet() == True:
    email('start')
    sys.exit()
else:
    sys.exit()
