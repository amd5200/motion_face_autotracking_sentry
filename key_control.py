#!/usr/bin/python

import serial
import curses
import time
from curses import wrapper #- See more at: http://ceilingmemo.blogspot.tw/2014/03/raspberry-pi_14.html#sthash.jlh89k9r.dpuf

arduino=serial.Serial('/dev/ttyUSB1',9600)

stdscr = curses.initscr()
stdscr.clear()


while True:
   
   ch = stdscr.getkey()
 # Quit 
   if ch == 'q':
      curses.endwin() 
      break
 # up
   if ch == 'w':
      arduino.write('2')
      print '2' 
 # left
   if ch == 'a':
      arduino.write('4')
      print '4' 
 # down
   if ch == 'x':
      arduino.write('8')
      print '8' 
 # right
   if ch == 'd':
      arduino.write('6')
      print '6' 

