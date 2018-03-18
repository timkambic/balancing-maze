import cv2
import numpy as np	

def nothing(x):
	pass
	
obj_color_low = np.array([0,0,0]) 
obj_color_high = np.array([0,0,0]) 
kernel = np.ones((7,7),np.uint8)

frame = cv2.imread('slika3 (8).jpg')
cv2.namedWindow('noNoise')
cv2.namedWindow('Control Panel')
cv2.moveWindow('noNoise',20,0)
cv2.moveWindow('Control Panel',20,0)
#cv2.resizeWindow('noNoise',700,400)

cv2.createTrackbar('lowHue','Control Panel',0,180,nothing)
cv2.createTrackbar('highHue','Control Panel',180,180,nothing)
cv2.createTrackbar('lowSaturation','Control Panel',0,255,nothing)
cv2.createTrackbar('highSaturation','Control Panel',255,255,nothing)
cv2.createTrackbar('lowBrightness','Control Panel',0,255,nothing)
cv2.createTrackbar('highBrightness','Control Panel',255,255,nothing)
cv2.createTrackbar('blur','Control Panel',1,10,nothing) # sesuje program ce prehitr slajdas


while(1):
	low_h = cv2.getTrackbarPos('lowHue','Control Panel')
	high_h = cv2.getTrackbarPos('highHue','Control Panel')
	low_s = cv2.getTrackbarPos('lowSaturation','Control Panel')
	high_s = cv2.getTrackbarPos('highSaturation','Control Panel')
	low_b = cv2.getTrackbarPos('lowBrightness','Control Panel')
	high_b = cv2.getTrackbarPos('highBrightness','Control Panel')
	obj_color_low = np.array([low_h,low_s,low_b])  
	obj_color_high = np.array([high_h,high_s,high_b]) 
	blur_v = cv2.getTrackbarPos('blur','Control Panel')
	if blur_v == 0:
		blur_v =1
		
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	blur = cv2.blur(hsv, (blur_v,blur_v))
	thresh = cv2.inRange(blur, obj_color_low, obj_color_high)
	noNoise = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)


	cv2.imshow("noNoise",noNoise)

	k = cv2.waitKey(1) & 0xFF
	if k == 27: # PRESS ESC TO QUIT PROGRAM
		break
#cap.release()	