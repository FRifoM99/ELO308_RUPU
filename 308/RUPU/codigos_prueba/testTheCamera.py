from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.rotation = 0
camera.hflip = False
camera.vflip = False
rawCapture = PiRGBArray(camera, size=(640, 480))

camera.start_preview()
time.sleep(5)
camera.stop_preview()
