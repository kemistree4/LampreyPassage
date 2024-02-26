# Imports
from picamera2 import Picamera2
import time
import RPi.GPIO as GPIO
import datetime 
import schedule
from picamera2.encoders import H264Encoder
import statistics

# Variables
camera = Picamera2()
BEAM_PIN = 17 # Pin we are using to read the IR break beam switch
video_config = camera.create_video_configuration()
camera.configure(video_config)
videos_recorded = 0
start_time = time.time()
encoder = H264Encoder(10000000)

# Setup the GPIO
GPIO.setmode(GPIO.BCM)                 # GPIO layout mode      
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup the gpio pin we are reading from as a pullup input

def test_video():
    global videos_recorded
    now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
    timestamp = datetime.datetime.now().strftime("%m%d%y %H%M%S")
    print("Recording test video")
    camera.start_recording(encoder, '/media/counter/EEL CR VID/videos/test_video_{}.h264'.format(timestamp)) #Recording video file to Lexar thumb drive
    time.sleep(15)
    print("Test video complete")
    camera.stop_recording()

alarm_lst = [0 for _ in range(50)]

def alarm_mod(new_value):
    alarm_lst.insert(0, new_value)
    alarm_lst.pop(-1)
    return alarm_lst

#Makes a test video everyday at 6 am and saves it to the test_video folder.
schedule.every().day.at("16:48").do(test_video)

# Loop checking the switch
while True:
    # Read the switch value
    input = GPIO.input(BEAM_PIN)
    alarm_lst = [0 for _ in range(50)]
    # If the GPIO reading goes from high to low, record for 30 secs
    try:
        if input != 0:
            #print("Checkpoint 1")
            time.sleep(2) # wait for 2 seconds
            if input != 0:
                #print("Checkpoint 2")
                # Check if 15 videos have been recorded in the last hour
                if videos_recorded >= 15 and (time.time() - start_time) < 3600:  # 3600 seconds = 1 hour
                    # Wait for 30 cycles of input being equal to 1
                    print("Too many files this hour. Deactivating until clear")
                    alarm_mod(1)
                    while statistics.mean(alarm_lst) > 0:
                        if GPIO.input(BEAM_PIN) == 1 and statistics.mean(alarm_lst) > 0:
                            #print("Checkpoint 3")
                            alarm_mod(1)
                            print(statistics.mean(alarm_lst))
                        if GPIO.input(BEAM_PIN) == 0:
                            alarm_mod(0)
                            #print(statistics.mean(alarm_lst))
                        if GPIO.input(BEAM_PIN) == 0 and statistics.mean(alarm_lst) == 0:
                            print("Condition clear. Reactivating")
                            break
                        time.sleep(1)  # Wait for 1 second before checking again
                    videos_recorded = 0  # Reset videos recorded count
                    start_time = time.time()  # Reset start time
                else:
                    #define time format for filenames and log output
                    now = time.localtime(time.time())      #Variable plugged into asci time to allow for readable date print out 
                    timestamp = datetime.datetime.now().strftime("%m%d%y %H%M%S") #Variable to update name of video files with current date and time
                    camera.start_recording(encoder, '/media/counter/EEL CR VID/videos/{}.h264'.format(timestamp)) #Recording video file to Lexar thumb drive
                    time.sleep(60)
                    camera.stop_recording()
                    videos_recorded += 1
                    time.sleep(0.05) #Debounce
        schedule.run_pending()  # Run scheduled tasks
    except:
        continue
        
