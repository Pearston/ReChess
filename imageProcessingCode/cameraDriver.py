# <------------ RASPBERRY PI ------------>

from picamera2 import Picamera2, Preview
import time

class ReChessCamera:
    def __init__(self):
        self.picam2 = Picamera2()
        #2MP  -> 10mm 1920, 1920
        #8MP  -> 7mm  3840, 3840
        #16   -> 5mm  
        camera_config = self.picam2.create_still_configuration(main={"size": (2320, 2320)}, lores={"size": (1920, 1920)}, display="main")
        # camera_config = picam2.create_preview_configuration(raw={"size": picam2.sensor_resolution})
        self.picam2.configure(camera_config)
        # picam2.start_preview(Preview.QTGL)
        self.picam2.start()


    def takeAPicture(self):
        
        time.sleep(0)
        self.picam2.capture_file("chessboard.jpg")

        # close camera so we can use in loop
        #self.close()

    def closeCamera(self):
        self.picam2.close()


    # <------------ MAC-OS ------------>
    # import cv2.aruco  as aruco
    # import cv2 as cv
    # import numpy as np
    # import os

    # def takeAPicture():
    #     cam = cv.VideoCapture(0)
    #     img = cam.read()[1]
    #     cv.imwrite('chessboard.jpg', img)
