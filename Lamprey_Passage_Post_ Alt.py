"""Testing the video recording settings"""
import datetime as dt
import os
from random import randint
import subprocess
import sys

import picamera


class Camera(object):
    """Camera device"""
    def __init__(self):
        self.device = None  # type: picamera.PiCamera
        self.stream = None  # type: picamera.PiCameraCircularIO

    def initialize_camera(self):
        """Initializes the camera to 1280x720 and start recording video to a circular buffer"""
        print "initializing camera"
        self.device = picamera.PiCamera()
        # set the camera's resolution (1280, 720)
        self.device.resolution = (1280, 720)
        # set the camera's framerate
        self.device.framerate = 24
        self.stream = picamera.PiCameraCircularIO(self.device, seconds=8)
        self.device.start_recording(self.stream, format='h264')
        return

    def stop_camera(self):
        """Stop the recording and turn the camera off"""
        if self.device is not None:
            if self.device.recording:
                self.device.stop_recording()
            self.device.close()
        if self.stream is not None:
            self.stream = None
        return

    def capture_video(self):
        """Store the video from the circular buffer to disk"""
        try:
            if self.device is None:
                # get the camera set up
                self.initialize_camera()
            video_name = dt.datetime.now().strftime(
                '%m-%d-%Y_%H:%M:%S').replace(':', '-') + '.h264'
            video_path = "/home/pi"
            # copy the buffer to disk
            print os.path.join(video_path, video_name)
            self.stream.copy_to(os.path.join(video_path, video_name), seconds=6)
            # add the MP4 wrapper to the h264 file using the MP4Box program
            mp4_command = "MP4Box -add '{0}' '{1}.mp4' -fps 24".format(
                os.path.join(video_path, video_name),
                os.path.join(video_path, os.path.splitext(os.path.basename(video_name))[0]))
            subprocess.call([mp4_command], shell=True)
            # remove the original h264 file
            os.remove(os.path.join(video_path, video_name))
        except BaseException as err:
            print 'error: {0} on line {1}\r'.format(err, sys.exc_info()[-1].tb_lineno)
        return


def main():
    """Main program"""
    camera = Camera()
    camera.initialize_camera()
    camera.device.wait_recording(timeout=randint(9, 20))
    camera.capture_video()
    camera.stop_camera()
    return


if __name__ == '__main__':
    main()
    sys.exit(0)
