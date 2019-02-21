import io
import time
import picamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, GPIO.PUD_UP)

with picamera.PiCamera() as camera:
    stream = picamera.PiCameraCircularIO(camera, seconds=20)
    camera.start_recording(stream, format='h264')
    GPIO.wait_for_edge(4, GPIO.FALLING)
    camera.wait_recording(30)
    camera.stop_recording()
    for frame in stream.frames:
        if frame.header:
            stream.seek(frame.position)
            break
    with io.open('/home/pi/Desktop/video.h264', 'wb') as output:
        while True:
            data = stream.read1()
            if not data:
                break
            output.write(data)
