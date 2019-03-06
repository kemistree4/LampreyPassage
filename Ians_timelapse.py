import time
import picamera
import datetime

with picamera.PiCamera() as camera:
    now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
    timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S") #Variable to update name of video files with current date and time
    camera.start_preview()
    time.sleep(1)
    for filename in camera.capture_continuous('/media/pi/C659-66D9/Lamprey_Images/{}.h264'.format(timestamp)):
        print('Captured %s' % filename)
        time.sleep(2) # wait 2 secs
