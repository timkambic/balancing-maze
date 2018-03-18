import cv2
import numpy as np	

def nothing(x):
	pass
	
obj_color_low = np.array([0,0,0])  #lower end -red
obj_color_high = np.array([0,0,0]) # higher end -red
kernel = np.ones((7,7),np.uint8)

#img = cv2.imread('slike/slika3 (7).jpg') #--------------------------------------------------------------- INPUT IMAGE !!!!
cap=cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_BRIGHTNESS,50)
cv2.namedWindow('noNoise')
cv2.namedWindow('Control Panel')
cv2.moveWindow('noNoise',20,0)
cv2.moveWindow('Control Panel',20,0)
cv2.resizeWindow('Control Panel',500,350)

cv2.createTrackbar('lowHue','Control Panel',20,180,nothing)
cv2.createTrackbar('highHue','Control Panel',160,180,nothing)
cv2.createTrackbar('lowSaturation','Control Panel',20,255,nothing)
cv2.createTrackbar('highSaturation','Control Panel',235,255,nothing)
cv2.createTrackbar('lowBrightness','Control Panel',20,255,nothing)
cv2.createTrackbar('highBrightness','Control Panel',230,255,nothing)
cv2.createTrackbar('blur','Control Panel',1,10,nothing) 


while(1):
	_, img = cap.read()
	#img = img[0:470, 80:556]# [0:720, 200:1140]
	cv2.imshow('org',img)
	
	low_h = cv2.getTrackbarPos('lowHue','Control Panel')
	high_h = cv2.getTrackbarPos('highHue','Control Panel')
	low_s = cv2.getTrackbarPos('lowSaturation','Control Panel')
	high_s = cv2.getTrackbarPos('highSaturation','Control Panel')
	low_b = cv2.getTrackbarPos('lowBrightness','Control Panel')
	high_b = cv2.getTrackbarPos('highBrightness','Control Panel')
	obj_color_low = np.array([low_h,low_s,low_b])  
	obj_color_high = np.array([high_h,high_s,high_b]) 
	
	img1 = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	blur_v = cv2.getTrackbarPos('blur','Control Panel')
	if blur_v != 0:
		img1 = cv2.blur(img1, (blur_v,blur_v))
	img1 = cv2.inRange(img1, obj_color_low, obj_color_high)
	noNoise = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernel)


	cv2.imshow("noNoise",noNoise)

	k = cv2.waitKey(1) & 0xFF
	if k == 27: # ------------------------------------------------------------------------------------- PRESS ESC TO QUIT PROGRAM
		break
	elif k == 115 | 112: #----------------------------------------------------------------------------- press 's' or 'p' to print selected values in console
		print "Low:", low_h,low_s,low_b
		print "High:", high_h,high_s,high_b ,"\n"
		
		
		