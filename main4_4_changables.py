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

'''
#kva bi lohk errorje povzrocal
-maze_array ma najprej y poj x 
-width/height zamenan ?


optimization of 2nd part
-don't display src (remove ...)


mogoce zamenat path_list z path_list_turn? 
'''


####################################################################	
#-----------SETUP------------
var = Variables()
#MAZE_SIZE_X = 8 # size of maze (number of tiles)
#MAZE_SIZE_Y = 8
#OBJ_COLOR_LOW = np.array([38,70,90])  #lower end of object/ball
#OBJ_COLOR_HIGH = np.array([83,195,250]) # higher end 
font = cv2.FONT_HERSHEY_PLAIN

#create windows to display images
cv2.namedWindow('src') 
cv2.namedWindow('cpy')
cv2.namedWindow('solved')
cv2.moveWindow('src', 0,0) # move windows so they don't overlap
cv2.moveWindow('cpy', 500,0)
cv2.moveWindow('solved',1000,0)
#initialize serial
serial = serial.Serial('COM8',9600) 
time.sleep(1) # wait to make sure serial is initialized 
print "\nSerial port is open?:",serial.isOpen()

brightness_led = 50 # brightness of leds located on top, 0-255
serial.write("15,15,"+str(brightness_led)+",") #level out maze

#--------END OF SETUP--------
###########################################################################

cap = cv2.VideoCapture(0)

for i in range(10): # wait for camera to get auto adjusted to brightness 
	_, img_src = cap.read()
	
_, img_src = cap.read()
path_list, img_maze_solved = mazeAnalysisAndStuff(img_src,var.MAZE_SIZE_X,var.MAZE_SIZE_Y) # find path through maze; returns: list of path tiles, image with data
cv2.imshow('solved',img_maze_solved)
if path_list is None:
	print "Path was not found \n Press any key to exit programm"
	cv2.waitKey(0)
	sys.exit()
cv2.waitKey(0)
##############################################################################
_, img_src = cap.read()
STEP_X,STEP_Y = calculateSTEP(img_src,var.MAZE_SIZE_X,var.MAZE_SIZE_Y)
end_x = STEP_X/2 + path_list[-1][0]*STEP_X # position of end in px
end_y = STEP_Y/2 + path_list[-1][1]*STEP_Y
	
	
nTarget = 1 #runs from 1 to len(path_list) # starting target maybe change to 0
nFPS = 0
nLoop =1
while True: # find ball and get it through maze
	loopTime = time.time() # starting time later used to calculate fps
	_, img_src = cap.read()
	img2 = img_src[0:470, 90:566] # for 640x480 video # create ROI
	img2_cpy = img2 # copy of img to draw on it
	img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV) #rgb -> hsb
	img2 = cv2.blur(img2, (3,3)) # blur img
	
	obj_x,obj_y,obj_w,obj_h = find_object(img2, var.OBJ_COLOR_LOW,var.OBJ_COLOR_HIGH) #find object using colour (returns -1 if object not found)
	x_object = obj_x + obj_w/2 # holds x coordinate of ball in px
	y_object = obj_y + obj_h/2 # holds y coordinate of ball in px
	if obj_x != -1: 
		cv2.rectangle(img2_cpy,(obj_x,obj_y),(obj_x+obj_w,obj_y+obj_h),(200,70,180),6) # draw rectangle around ball
		cv2.circle(img2_cpy,(x_object,y_object),3,(0,0,250),-1) #and circle in the middle of it
		
	targetX = STEP_X/2 + path_list[nTarget][0]*STEP_X # position of the next target
	targetY = STEP_Y/2 + path_list[nTarget][1]*STEP_Y
	
	delta_x = targetX - x_object # the difference between current position and desired position 
	delta_y = targetY - y_object
	
	
	#send data to arduino via serial port
	data_str=str(targetX)+","+str(x_object)+","+str(targetY)+","+str(y_object)+","+str(brightness_led)+","
	serial.write(data_str)
	print delta_x,delta_y
	
	
	if isNear(x_object,y_object, targetX,targetY): # ball is near desired position -> set next target
		print "ball passed ",nTarget, " -", path_list[nTarget]
		nTarget +=1
	
	
	k = cv2.waitKey(1) & 0xFF
	if k == 27: # esc
		print "program stopped"
		break
	if isNear(x_object,y_object, end_x,end_y): # ball is at the end position
		print "\nSUCCESS !!  ball is at the end of the maze"
		break
	
	nFPS += 1/(time.time()-loopTime) # fps calculation
	fps= nFPS/nLoop 
	nLoop+=1 #used for fps calculation
	
	#display images 
	cv2.putText(img2_cpy, "fps:" + str(int(fps)) ,(410,25), font, 1,(10,0,255),1,cv2.LINE_AA)
	cv2.putText(img2_cpy,"next target: "+str(path_list[nTarget]),(10,25), font, 1.5,(10,0,255),1,cv2.LINE_AA)
	cv2.imshow('src', img2)
	cv2.imshow('cpy', img2_cpy)
	
	
#clean exit
cap.release()
serial.close()