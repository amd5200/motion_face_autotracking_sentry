#!/usr/bin/python
# coding: utf -8                   #加上這行才能key中文 要import urllib2
import urllib2
import sys
import cv2.cv as cv
import cv2
from optparse import OptionParser
import serial
import time

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size

min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0
arduino=serial.Serial('/dev/ttyUSB1',9600)

#width = 160 #leave None for auto-detection
#height = 120 #leave None for auto-detection
width = 640 #leave None for auto-detection
height = 480 #leave None for auto-detection

def detect_and_draw(img, cascade):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                   cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

#######   若解析度有改變，下面劃線座標亦隨之改變##############
    '''
    cv.Line(img, (210,0),(210,480), (0,255,255),1) 
    cv.Line(img, (420,0),(420,480), (0,255,255),1) 
    cv.Line(img, (0,160),(640,160), (0,255,255),1) 
    cv.Line(img, (0,320),(640,320), (0,255,255),1)
    '''
    cv.Line(img, (width/2,0),(width/2,height), (0,10,255),3) 
    cv.Line(img, ((width/2-20),(height/2-10)),((width/2-20),(height/2+10)), (0,10,255),2)
    cv.Line(img, ((width/2+20),(height/2-10)),((width/2+20),(height/2+10)), (0,10,255),2) 
    cv.Line(img, (0,height/2),(width,height/2), (0,10,255),3) 
    cv.Line(img, ((width/2-10),(height/2-20)),((width/2+10),(height/2-20)), (0,10,255),2)
    cv.Line(img, ((width/2-10),(height/2+20)),((width/2+10),(height/2+20)), (0,10,255),2)
    
    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
##################################################################################################3333
                cx = (int(x * image_scale) + int((x + w) * image_scale)) / 2
                cy = (int(y * image_scale) + int((y + h) * image_scale)) / 2
                print cx, cy
####################################################
                if cx < img.width*3/ 7 :
                     arduino.write('4')
                     print '4'
		if cx < img.width*2/ 7 :
                     arduino.write('44')
                     print '4'
		if cx < img.width/ 7 :
                     arduino.write('4444')
                     print '44'

                if cx > img.width*4 / 7 :
                     arduino.write('6')
                     print '6'
                if cx > img.width*5/ 7 :
                     arduino.write('66')
                     print '6'
                if cx > img.width*6/ 7 :
                     arduino.write('6666')
                     print '66'
                if cy < img.height*3/ 7:
                     arduino.write('2')
                     print '2'
                if cy < img.height*2/ 7:
                     arduino.write('22')
                     print '2'
                if cy < img.height/ 7:
                     arduino.write('2222')
                     print '222'
                if cy > img.height*4 / 7:
                     arduino.write('8')
                     print '8'
                if cy > img.height*5 / 7:
                     arduino.write('88')
                     print '8'
                if cy > img.height*6 / 7:
                     arduino.write('8888')
                     print '888'
		break
######################################################

    cv.ShowImage("result", img)

if __name__ == '__main__':
    cascade = cv.Load("haarcascade_frontalface_alt.xml")
    #cascade = cv.Load("cars3.xml")
    capture = cv.CreateCameraCapture(2)                   # camera   NO. 0, 1, 2
    print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)

    cv.NamedWindow("result", 1)
    frame = cv.QueryFrame(capture)
    
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)

            if not frame:
                #print 'hehe'
                #cv.WaitKey(0)
                continue#break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)

            detect_and_draw(frame_copy, cascade)

            if cv.WaitKey(10) == 27:
                break

    cv.DestroyWindow("result")
