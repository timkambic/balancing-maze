import sys
import time
import cv2
import numpy as np
from a_star_lib import AStarGrid, AStarGridNode
from itertools import product

#################################################################################################################################################
def make_graph(mapinfo):
	#makes graph for use with a*star algorithm 
	#input: maze size(w,h) , obstacle list
    nodes = [[AStarGridNode(x, y) for y in range(mapinfo['height'])] for x in range(mapinfo['width'])]
    graph = {}
    for x, y in product(range(mapinfo['width']), range(mapinfo['height'])):
        node = nodes[x][y]
        graph[node] = []
        for i, j in product([-1, 0, 1], [-1, 0, 1]):
            if not (0 <= x + i < mapinfo['width']): continue
            if not (0 <= y + j < mapinfo['height']): continue
            if [x+i,y+j] in mapinfo['obstacle']: continue
            graph[nodes[x][y]].append(nodes[x+i][y+j])
    return graph, nodes

#################################################################################################################################################	
def calculateSTEP(img,m_size_x,m_size_y):  
	#calculate the size of one tile, used for conversion from list to px
	img = img[0:470, 80:556] # for 640x480 -------------------------------------------------------------------------------------------------------CHANGE HERE
	img_height,img_width = img.shape[:2]
	STEP_X = img_width / m_size_x # size of one tile in px
	STEP_Y = img_height / m_size_y 
	return STEP_X,STEP_Y

#################################################################################################################################################
def isNear(x,y,end_x,end_y):
	errorX = 20 #--------------------------------------------------------------------------------------------------------------------------------CHANGE HERE
	errorY = 20
	if (x < end_x+errorX) & (x > end_x-errorX) & (y < end_y+errorY) & (y > end_y-errorY): return 1
	else : return 0

#################################################################################################################################################	
def mazeAnalysisAndStuff(img_src,MAZE_SIZE_X,MAZE_SIZE_Y):
	# takes an image of maze and analyses it to get the optimal path from entrance to the end
	# must edit start/end nodes later in the code
	BORDER_V = 85 # defines the colour border between obstacle or free path ------------------------------------------------------------------------CHANGE HERE
	maze_array = [[0 for x in range(MAZE_SIZE_X)]for x in range(MAZE_SIZE_Y)] # to hold 2d 'image' of maze, 1-obstacle, 0-free # najprej y, poj x !!!!!!
	
	
	img1 = img_src[0:470, 90:566] # for 640x480 #[0:720, 200:1140]  for 1280x720
	img1_cpy = img1
	img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
	img1 = cv2.blur(img1, (3,3)) # ni nujn

	img_height,img_width = img1.shape[:2]
	STEP_X = img_width / MAZE_SIZE_X # size of one tile in px
	STEP_Y = img_height / MAZE_SIZE_Y # size of one tile in px
	print "Image width/height:",img_width,"x", img_height
	print "Roi size:", STEP_X,"x", STEP_Y, "\n"

	txt_file = open('output_file.txt', 'w') # outputs maze array in .txt file


	for y in range(MAZE_SIZE_Y):   # divide img in x*y roi-s and decides whether its obstacle or not
		for x in range(MAZE_SIZE_X):
			img_roi = img1[y*STEP_Y:(y+1)*STEP_Y, x*STEP_X:(x+1)*STEP_X]
			avg_value,_2,_3,_4 = cv2.mean(img_roi) # only the first number -hsv?? 
			if avg_value > BORDER_V: # tile is obstacle
				txt_file.write(" 1 ")
				maze_array[y][x] = 1
			else:
				txt_file.write(" 0 ")	
		txt_file.write("\n")	
	print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in maze_array])) # prints maze_array in console	

	# ---change full 2d maze array into list of obstacles ---
	obstacle_list = [] 
	ab = 0
	for y in range(MAZE_SIZE_Y):
		for x in range(MAZE_SIZE_X):
			if maze_array[y][x] == 1:
				obstacle_list.append([])
				obstacle_list[ab].append(x)
				obstacle_list[ab].append(y)
				ab = ab+1
	#print "\n Obstacle list:", obstacle_list			

	#---MAZE SOLVING---
	graph, nodes = make_graph({"width": MAZE_SIZE_X, "height": MAZE_SIZE_Y, "obstacle": obstacle_list})
	paths = AStarGrid(graph)
	startNode, endNode = nodes[0][1], nodes[6][0] # ----------------------------------------------------------------- ------------------------------------start / end nodes !
	path = paths.search(startNode, endNode)
	path_list = []
	if path is None:
		print "\n No path found... "
		#sys.exit("Exiting program")
		return None ,img1_cpy # ----------------------------------------------------------------------------------------------------------- what should be first parameter
	else:
		print "\n Path found:", path
	
	#--change from 'tuple-list' to list-list--
	path_list = []
	for m in range(len(path)):
		tmp_string = str(path[m])
		path_list.append([])
		path_list[m].append(int(tmp_string[1]))
		path_list[m].append(int(tmp_string[3]))
	#print "\n Path list:", path_list

	#---make a list of the tiles where the path changes its direction---
	path_list_turns=[]
	direction1 = 2 # starting so it always gets added to the list
	count1 = 0
	for point in range(len(path_list)-1):
		if path_list[point][0] == path_list[point+1][0]: # x1=x2 - horizontal
			direction2 = 1
		else: # vertical
			direction2 = 0
		
		if direction2 != direction1: # direction changes -> add point to the list
			path_list_turns.append([])
			path_list_turns[count1].append(path_list[point][0])
			path_list_turns[count1].append(path_list[point][1])
			count1 +=1
		direction1 = direction2
	# add ending tile to list
	path_list_turns.append([])
	path_list_turns[count1].append(path_list[-1][0])
	path_list_turns[count1].append(path_list[-1][1])

	#--draw circles on path tiles--
	for s in range(len(path_list_turns)): # on path
		cv2.circle(img1_cpy, (STEP_X/2 + path_list_turns[s][0]*STEP_X , STEP_Y/2 + path_list_turns[s][1]*STEP_Y) , 15 ,(50,250,50),-1) 
	for n in range(len(path_list)): # on turning tiles
		cv2.circle(img1_cpy, (STEP_X/2 + path_list[n][0]*STEP_X , STEP_Y/2 + path_list[n][1]*STEP_Y) , 6 ,(0,0,250),-1) 		
	#draw grid for debugging
	for p in range(MAZE_SIZE_X):
		cv2.line(img1_cpy,(p*STEP_X,0),(p*STEP_X,MAZE_SIZE_Y*STEP_Y),(250,100,0))
	for r in range(MAZE_SIZE_Y):
		cv2.line(img1_cpy,(0,r*STEP_Y),(MAZE_SIZE_X*STEP_X,r*STEP_Y),(250,100,0))		
		
	return path_list_turns,img1_cpy

#################################################################################################################################################
def find_object(frame, low_end_color, high_end_color): 
	# find object of specific colour- between low_ and high_ end_color
	# example of low_end_color: OBJ_COLOR_LOW = np.array([38,70,90]) <- HSB values
	kernelM = np.ones((7,7),np.uint8) # for morphology
	thresh = cv2.inRange(frame, low_end_color, high_end_color)
	noNoise = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelM)
	#find object
	_2, contours, hierarchy = cv2.findContours(noNoise,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	maxArea =0
	if len(contours) > 0: 
		for cnt in contours: #find the largest object
			area = cv2.contourArea(cnt)
			if area > maxArea:
				maxArea = area
				best_cnt = cnt
		x2,y2,w2,h2 = cv2.boundingRect(best_cnt)
		return x2,y2,w2,h2
	else:
		return -1,-1,-1,-1
