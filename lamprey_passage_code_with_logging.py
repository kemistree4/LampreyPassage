# Imports
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import datetime 
import schedule

# Variables
camera = PiCamera()
BEAM_PIN = 4                                # Pin we are using to read the IR break beam switch
log_time = datetime.datetime.now().strftime('%m%d%y')
videos_recorded = 0
start_time = time.time()

# Setup the GPIO
GPIO.setmode(GPIO.BCM)                 # GPIO layout mode      
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup the gpio pin we are reading from as a pullup input

def test_video():
    global videos_recorded
    now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
    timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S")
    camera.start_recording('/media/pi/F8AF-129D/test_videos/{}.h264'.format(timestamp)) #Recording video file to Lexar thumb drive
    camera.wait_recording(15)
    camera.stop_recording()
    time.sleep(0.5)

#Makes a test video everyday at 6 am and saves it to the test_video folder.
schedule.every().day.at("06:00").do(test_video)

# Loop checking the switch
while True:
    # Read the switch value
    input = GPIO.input(BEAM_PIN)
    # If the GPIO reading goes from high to low, record for 30 secs
    if input != 1:
        time.sleep(2) # wait for 2 seconds
        now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
        timestamp = datetime.datetime.now().strftime("%m%d%y_%H%M%S") #Variable to update name of video files with current date and time
        if input != 1:
            # Check if 15 videos have been recorded in the last hour
            if videos_recorded >= 15 and (time.time() - start_time) < 3600:  # 3600 seconds = 1 hour
                # Wait for 30 cycles of input being equal to 1
                count = 0
                while count < 30:
                    if GPIO.input(BEAM_PIN) == 1:
                        count += 1
                    else:
                        count = 0
                    time.sleep(1)  # Wait for 1 second before checking again
                videos_recorded = 0  # Reset videos recorded count
                start_time = time.time()  # Reset start time
            else:
                #define time format for filenames and log output
                camera.start_recording('/media/pi/F8AF-129D/videos/{}.h264'.format(timestamp)) #Recording video file to Lexar thumb drive
                camera.wait_recording(30)
                camera.stop_recording()
                videos_recorded += 1
                time.sleep(0.05) #Debounce wait
    schedule.run_pending()  # Run scheduled tasks
