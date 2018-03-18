# variables to be used vith main*_*
import numpy as np


class Variables():
	MAZE_SIZE_X = 8 #number of tiles
	MAZE_SIZE_Y = 8
	
	OBJ_COLOR_LOW = np.array([38,70,90])  #lower end of object/ball for detection 
	OBJ_COLOR_HIGH = np.array([83,195,250]) # higher end 
	
	#SERIAL_PORT = 'COM8' # serial port for arduino 