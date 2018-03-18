import cv2
import numpy as np
import time
from pid_controller import*
import serial
from my_functions import *



OBJ_COLOR_LOW = np.array([37,79,57])  #lower end of object/ball
OBJ_COLOR_HIGH = np.array([97,255,200]) # higher end 

font = cv2.FONT_HERSHEY_PLAIN

#cv2.namedWindow('src') #create windows to display images
cv2.namedWindow('cpy')
#cv2.moveWindow('src', 0,0) # move windows so they don't overlap
cv2.moveWindow('cpy', 500,0)

serial = serial.Serial('COM8',9600) #initialize serial
time.sleep(1) # wait to make sure serial is initialized 
print "\nSerial port is open?:",serial.isOpen()
brightness_led = 50 # brightness of leds located on top, 0-255
serial.write("15,15,"+str(brightness_led)+",") #level out maze

cap = cv2.VideoCapture(0)

pid_x = PID_controller()
#pid_y = PID_controller()

Kp = 0.035
Ki  = 0.05
Kd = 0



targetX=233
targetY=235
	
pid_x.Initialize(Kp,Ki,Kd)
#pid_y.Initialize(Kp,Ki,Kd)
	
nFPS = 0
nLoop =1
while True: # find ball and get it through maze
	loopTime = time.time() # starting time later used to calculate fps
	_, img_src = cap.read()
	img2 = img_src[0:470, 90:566] # for 640x480 video # create ROI
	img2_cpy = img2 # copy of img to draw on it
	img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV) #rgb -> hsb
	img2 = cv2.blur(img2, (3,3)) # blur img
	
	obj_x,obj_y,obj_w,obj_h = find_object(img2, OBJ_COLOR_LOW,OBJ_COLOR_HIGH) #find object using colour (returns -1 if object not found)
	x_object = obj_x + obj_w/2 # holds x coordinate of ball in px
	y_object = obj_y + obj_h/2 # holds y coordinate of ball in px
	if obj_x != -1: 
		cv2.rectangle(img2_cpy,(obj_x,obj_y),(obj_x+obj_w,obj_y+obj_h),(200,70,180),6) # draw rectangle around ball
		cv2.circle(img2_cpy,(x_object,y_object),3,(0,0,250),-1) #and circle in the middle of it
		
	delta_x = targetX - x_object # the difference between current position and desired position 
	delta_y = targetY - y_object
	
	pid_x_out = pid_x.Compute(delta_x) +15
	pid_y_out = 15#(pid_y.Compute(delta_y) +15)*-1 +30
	
	pid_x_out = int(round(pid_x_out,0))
	pid_y_out = int(round(pid_y_out,0))

	#send data to arduino via serial port
	data_str=str(pid_x_out)+","+str(pid_y_out)+",0,"
	serial.write(data_str)

	print "X- dx:",delta_x,"PID:",pid_x_out,     "\tY- dy:",delta_y,"PID:",pid_y_out
	
	k = cv2.waitKey(1) & 0xFF
	if k == 27: # esc
		print "program stopped"
		break

	nFPS += 1/(time.time()-loopTime) # fps calculation
	fps= nFPS/nLoop 
	nLoop+=1 #used for fps calculation
	#display images 
	cv2.putText(img2_cpy, "fps:" + str(int(fps)) ,(410,25), font, 1,(10,0,255),1,cv2.LINE_AA)
	#cv2.imshow('src', img2)
	cv2.imshow('cpy', img2_cpy)
	
	
#clean exit
serial.write("15,15,0,")
cap.release()
serial.close()