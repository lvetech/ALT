#!python3

import numpy as np
import picamera #Please see http://picamera.readthedocs.io for the 'picamera' library documentation.
                #As of the moment of writing this comment, the latest 'picamera' library version is 1.12.
import picamera.array
import time
import datetime
import os


experimentDurationHours = 0.5 #Duration of the ALT data collection, hours.
timeSliceDurationMinutes = 6 #The whole 'experimentDurationHours' time is split into 'timeSliceDurationMinutes' minutes long intervals (‘time slices’).
experimentDir = "./experiment/" #Location where ALT data, video, etc. will be saved. Each 'time slice' has its own sub-folder, see below.

os.makedirs(experimentDir) #Error if the 'experimentDir' folder exists.

#Please see http://picamera.readthedocs.io/en/release-1.12/api_array.html#pimotionanalysis
#for the 'picamera.array.PiMotionAnalysis' class documentation.
class ALT(picamera.array.PiMotionAnalysis):

    def analyse(self, a):

        #This is the 'sSAD' value referred to in the 'Readme.md' file:
        sSAD = np.sum(a['sad'])
        sSADs.append(sSAD)

        #Note that the 'sSAD' value for an I-frame in the captured video data stream will be equal to zero.
        #Please consult documentation for the 'start_recording()' method of the 'picamera.PiCamera' class
        #(http://picamera.readthedocs.io/en/release-1.12/api_camera.html#picamera.PiCamera.start_recording).
        #Particularly, setting the 'intra_period' parameter of the 'start_recording()' method to zero will
        #cause "the encoder to produce a single initial I-frame, and then only P-frames subsequently".
        #If you would like to keep I-frames in the captured video stream, you can adjust the 'intra_period' parameter accordingly (or leave it at its default value).
        #A very primitive way to process the I-frame 'sSAD' values would be to replace them with the 'sSAD' value of the previous frame,
        #as the following 'pseudo code' shows:

        #if sSAD != 0:
            #sSADsNoZeros.append(sSAD)
        #else:
            #if len(sSADsNoZeros) >= 1:
                #sSADsNoZeros.append(sSADsNoZeros[-1])


#The relevant sections of the 'picamera' library documentation for the following sections of the ALT code are:
#http://picamera.readthedocs.io/en/release-1.12/recipes1.html#capturing-consistent-images
#and
#http://picamera.readthedocs.io/en/release-1.12/api_camera.html#picamera.PiCamera.start_recording
with picamera.PiCamera() as camera:

    with ALT(camera) as mvdOutput: # motion vector data (mvd) output

        camera.resolution = (1280, 720)
        camera.framerate = 49
        camera.exposure_mode = 'night'
        camera.awb_mode = 'auto'
        camera.iso = 1600
        camera.sharpness = 100
        camera.contrast = 100

        while camera.analog_gain <= 1:
            time.sleep(0.1)

        #'seep' delays below give you some time before the camera parameters are locked and video recording and ALT data collection start
        #which might be helpful, for example, if you start ALT before going to sleep
        #so that there is time for you to turn the lights off and let the camera adjust to low-light environment.
        print('Preparing ...')
        print('60 ...')
        time.sleep(45)
        print('15 ...')
        time.sleep(5)

        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g

        print('10 ...')
        time.sleep(5)
        print('5 ...')
        time.sleep(5)

        print('RUNNING ...')

        for t in range(int(experimentDurationHours*60/timeSliceDurationMinutes)):

            startDateTime = datetime.datetime.now()

            timeSliceDir = experimentDir + str(startDateTime) + "/"
            print('timeSliceDir = ', timeSliceDir)
            os.makedirs(timeSliceDir)

            sSADs = []
            sSADsfile = open(timeSliceDir + 'SADs.txt', 'w')

            #Note that the 'quality' parameter of the 'start_recording()' method might be useful to keep the size of the captured video files reasonably low.
            #Please see 'http://picamera.readthedocs.io/en/release-1.12/api_camera.html#picamera.PiCamera.start_recording'
            #for details.
            camera.start_recording(timeSliceDir + '1280x720.h264', format = 'h264', motion_output = mvdOutput)
            camera.wait_recording(timeSliceDurationMinutes*60)
            camera.stop_recording()

            #Note that saving ALT data into a file and stopping/restarting video recording will cause
            #a short time 'gap' between the consecutive 'time slices'
            for i in range(len(sSADs)):
                sSADsfile.write(str(i + 1) + ": " + str(sSADs[i]) + "\n")

            sSADsfile.close()
