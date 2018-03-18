# Tim Kambic, april/maj 2015
# Using open-cv get the 2d array of 1s and 0s representing maze out of picture. Then use A* path-finding algorithm to find the shortest path out of it. Using colour tracking and 
# servos (connected to arduino uno) "navigate" ball out of it
#
# additional files needed: my_functions.py, a_star_lib.py
import time
import sys
import cv2
import numpy as np
import serial

from my_functions import *
from changeables import Variables
from simple_controller import Controller_simple

#***************************************************************************************

class CONTROLL_MAIN():
	def __init_(self):
		self.MAZE_SIZE_X = 1
		self.MAZE_SIZE_Y =1 # ??
		
	def Initialize(self,maze_x,maze_y,low_c,high_c): #input from changeable-variables
		self.MAZE_SIZE_X = maze_x
		self.MAZE_SIZE_Y = maze_y
		self.OBJ_COLOR_LOW = low_c
		self.OBJ_COLOR_HIGH = high_c		
		
		#init serial
		self.serial = serial.Serial('COM8',9600)
		time.sleep(1) # wait to make sure serial is initialized 
		print "\nSerial port is open?:",self.serial.isOpen()
		self.brightness_led = 50
		self.serial.write("15,15,"+str(self.brightness_led)+",") #level out maze
		
		#set controller for motors
		self.motor_controll = Controller_simple()
		#set video capture
		self.cap = cv2.VideoCapture(0)
		for i in range(10): # wait for camera to get auto adjusted to brightness 
			self.cap.read()
		_,img_src = self.cap.read()
		self.STEP_X,self.STEP_Y = calculateSTEP(img_src,self.MAZE_SIZE_X,self.MAZE_SIZE_Y)	
	
	
	def Init_display(self):
		cv2.namedWindow('src') 
		cv2.namedWindow('cpy')
		cv2.namedWindow('solved')
		cv2.moveWindow('src', 0,0) # move windows so they don't overlap
		cv2.moveWindow('cpy', 500,0)
		cv2.moveWindow('solved',1000,0)
		
		self.font = cv2.FONT_HERSHEY_PLAIN
		
	def cv_display_current(self):	
		cv2.putText(self.img2_cpy, "fps:" + str(int(self.fps)) ,(410,25), self.font, 1,(10,0,255),1,cv2.LINE_AA)
		cv2.putText(self.img2_cpy,"next target: "+str(self.path_list[self.nTarget]),(10,25), self.font, 1.5,(10,0,255),1,cv2.LINE_AA)
		#cv2.imshow('src', img2)
		cv2.imshow('cpy', self.img2_cpy)
	def cv_display_path(self):
		cv2.imshow('solved',self.img_maze_solved)

	def EXIT(self):
			self.serial.write("15,15,"+"0"+",")
			self.cap.release()
			self.serial.close()
	
	def Analyse_maze(self):
		_,img_src = self.cap.read()
		self.path_list,self.img_maze_solved = mazeAnalysisAndStuff(img_src,self.MAZE_SIZE_X,self.MAZE_SIZE_Y)
		if self.path_list is None:
			print "Path was not found \n Press any key to exit program"
			cv2.waitKey(0)
			sys.exit()
		else:
			print "Press any key to proceed"
			cv2.waitKey(0)
		# setup for DoStuff
		_,img_src = self.cap.read()
		#self.STEP_X,self.STEP_Y = calculateSTEP(img_src,self.MAZE_SIZE_X,self.MAZE_SIZE_Y)
		self.end_x = self.STEP_X/2 + self.path_list[-1][0]*self.STEP_X # position of end in px
		self.end_y = self.STEP_Y/2 + self.path_list[-1][1]*self.STEP_Y
		self.nTarget = 1
		self.nFPS = 0
		self.nLoop =1
		
	def DoStuff(self):
		loopTime = time.time()
		_, img_src = self.cap.read()
		img2 = img_src[0:470, 90:566] # for 640x480 video # create ROI
		self.img2_cpy = img2 # copy of img to draw on it
		img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV) #rgb -> hsb
		img2 = cv2.blur(img2, (3,3)) # blur img
		
		obj_x,obj_y,obj_w,obj_h = find_object(img2, self.OBJ_COLOR_LOW,self.OBJ_COLOR_HIGH) #find object using colour (returns -1 if object not found)
		x_object = obj_x + obj_w/2 # holds x coordinate of ball in px
		y_object = obj_y + obj_h/2 # holds y coordinate of ball in px

		if obj_x != -1: 
			cv2.rectangle(self.img2_cpy,(obj_x,obj_y),(obj_x+obj_w,obj_y+obj_h),(200,70,180),6) # draw rectangle around ball
			cv2.circle(self.img2_cpy,(x_object,y_object),3,(0,0,250),-1) #and circle in the middle of it
		
		targetX = self.STEP_X/2 + self.path_list[self.nTarget][0]*self.STEP_X # position of the next target
		targetY = self.STEP_Y/2 + self.path_list[self.nTarget][1]*self.STEP_Y
		
		delta_x = targetX - x_object # the difference between current position and desired position 
		delta_y = targetY - y_object
		
		output_x, output_y = self.motor_controll.Compute(delta_x,delta_y)
		data_str = str(output_x)+","+str(output_y)+","+str(self.brightness_led)+","
		#send data to arduino via serial port
		self.serial.write(data_str)
		print delta_x,delta_y
		
		if isNear(x_object,y_object, targetX,targetY): # ball is near desired position -> set next target
			print "ball passed ",self.nTarget, " -", self.path_list[self.nTarget]
			self.nTarget +=1
			time.sleep(0.5)
		if isNear(x_object,y_object, self.end_x,self.end_y): # ball is at the end position
			print "\nSUCCESS !!  ball is at the end of the maze"
			sys.exit("ball at the end")
		
		#fps
		self.nFPS +=1/(time.time()-loopTime)
		self.fps = self.nFPS/self.nLoop
		self.nLoop+=1
		
		k = cv2.waitKey(1) & 0xFF
		if k == 27: # esc
			self.EXIT()
			sys.exit("Esc pressed - exiting program")
			
		
			
#***************************************************************************************
####################################################################	
#-----------SETUP------------
var = Variables()
cont = CONTROLL_MAIN()
cont.Initialize(var.MAZE_SIZE_X,var.MAZE_SIZE_Y,var.OBJ_COLOR_LOW,var.OBJ_COLOR_HIGH)
cont.Init_display()

#--------END OF SETUP--------

cont.Analyse_maze()
cont.cv_display_path
while True:
	cont.DoStuff()
	cont.cv_display_current()








