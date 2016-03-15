#!/usr/bin/python
# coding: utf -8                   #加上這行才能key中文 要import urllib2
import urllib2
import cv2.cv as cv
import sys
import serial
import time

arduino=serial.Serial('/dev/ttyUSB1',9600)     #set arduino serial port

cv.NamedWindow("color_tracking", 1)

#創建一個矩形，來讓我們在圖片上寫文字，參數依次定義了文字類型，高，寬，字體厚度等。
font=cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 4)

#capture = cv.CaptureFromCAM(0)
#capture = cv.CaptureFromCAM(1)
capture = cv.CaptureFromCAM(2)

#width = 160 #leave None for auto-detection
#height = 120 #leave None for auto-detection
width = 640 #leave None for auto-detection
height = 480 #leave None for auto-detection
middle_w = 2 #Cross Center width 十字中心歸零校正,數字越大線往左
middle_h = 2 #Cross Center height 十字中心歸零校正,數字越大線往上
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height)

while True:
    img = cv.QueryFrame(capture)
    cv.Smooth(img, img, cv.CV_BLUR,3)
    hue_img = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.CvtColor(img, hue_img, cv.CV_BGR2HSV)

    threshold_img = cv.CreateImage(cv.GetSize(hue_img), 8, 1)
    #Python: cv.InRangeS(src, lower, upper, dst) http://www.colorspire.com/
    #cv.InRangeS(hue_img, (38,120,60), (75,255,255), threshold_img)          # color code green
    cv.InRangeS(hue_img, (100,120,60), (200,255,255), threshold_img)          # color code blue
    #cv.InRangeS(hue_img, (0,100,60), (10,255,255), threshold_img)           # color code red
    
    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(threshold_img, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)

    points = []
    while contour:
        rect = cv.BoundingRect(list(contour))
        contour = contour.h_next()
        size = (rect[2] * rect[3])
        if size > 100:
            pt1 = (rect[0], rect[1])
            pt2 = (rect[0] + rect[2], rect[1] + rect[3])
            cv.Rectangle(img, pt1, pt2, cv.CV_RGB(255,0,0), 3)
########################################  contour center  ####################################################
                
            cx = (rect[2]/2 + rect[0])              #(0,0)################
            cy = (rect[3]/2 + rect[1])              ######################   
            print cx, cy                            ######################<--160x120 pix
                                                    ######################
                                                    ############(160,120)#
#將文字框加入到圖片中，(5,30)定義了文字框左頂點在窗口中的位置，最後參數定義文字顏色
            
            if cx <= (width*1/2) and cy >= (height*1/2) :
                 TestStr = "Locking"
                 cv.PutText(img, TestStr , (5,30), font, (0,0,255))
            else:
                 TestStr = "serching...."
                 cv.PutText(img, TestStr , (5,30), font, (0,255,0))
######################################### servo motor ######################################################
            if cx < width*3/ 7 :
                 arduino.write('4')
                 print '4'
            if cx < width*2/ 7 :
                 arduino.write('44')
                 print '4'
            if cx < width/ 7 :
                 arduino.write('4444')
                 print '44'

            if cx > width*4 / 7 :
                 arduino.write('6')
                 print '6'
            if cx > width*5/ 7 :
                 arduino.write('66')
                 print '6'
            if cx > width*6/ 7 :
                 arduino.write('6666')
                 print '66'
            if cy < height*3/ 7:
                 arduino.write('2')
                 print '2'
            if cy < height*2/ 7:
                 arduino.write('22')
                 print '2'
            if cy < height/ 7:
                 arduino.write('2222')
                 print '222'
            if cy > height*4 / 7:
                 arduino.write('8')
                 print '8'
            if cy > height*5 / 7:
                 arduino.write('88')
                 print '8'
            if cy > height*6 / 7:
                 arduino.write('8888')
                 print '888'
            break                

####################################################################################################################### 
    ######   若解析度有改變，下面劃線座標亦隨之改變##############
    cv.Line(img, (width/middle_w,0),(width/middle_w,height), (0,10,255),2) 
    cv.Line(img, ((width/middle_w-20),(height/middle_h-10)),((width/middle_w-20),(height/middle_h+10)), (0,10,255),1)
    cv.Line(img, ((width/middle_w+20),(height/middle_h-10)),((width/middle_w+20),(height/middle_h+10)), (0,10,255),1) 
    cv.Line(img, (0,height/middle_h),(width,height/middle_h), (0,10,255),2) 
    cv.Line(img, ((width/middle_w-10),(height/middle_h-20)),((width/middle_w+10),(height/middle_h-20)), (0,10,255),1)
    cv.Line(img, ((width/middle_w-10),(height/middle_h+20)),((width/middle_w+10),(height/middle_h+20)), (0,10,255),1)

    cv.ShowImage("color_tracking", img)
    cv.ShowImage("threshold", threshold_img)
    if cv.WaitKey(10) == 27:
        break
