#!/usr/bin/env python
"""@package docstring
Documentation for this module.
This code implements the dijskstra algorithm to find the distance transform of a given occupancy grid map
"""
import IPython
import sys
import numpy as np
from parser import parser
from pylab import *
from PriorityQueue import PriorityQueue

def get_cost(state):
	"""Input: Cost map and State 
   	Output: The Cost of the queried state
   	This function returns Cost of each cell in the input image map 
   	"""
	(x,y) = state
	return C[x][y]

def inBounds(state):
	"""Input: State 
   	Output: Bool value whether the state is in bounds or not
   	This function returns whether the queried state is in bounds of the image or not
    	"""
	(x,y) = state
	return 0<=x<M and 0<=y<N

def get_successors(state):
	"""Input: State 
   	Output: Successors of the queried state
   	This function assumes a four connected gridworld and outputs the successors of the current state
    	"""
	(x,y) = state
	successors = [(x[0]+1,x[1]),(x[0],x[1]-1),(x[0]-1,x[1]),(x[0],x[1]+1)]
	successors = filter(inBounds,successors)
	return successors

def dijkstra(start,C):
	"""Input: Start state and Cost map
	Output: The cost of each cell as a dictionary
	This function performs the Dijkstra algorithm to find the cost of each cell in the map
	"""
	openSet = PriorityQueue()
	openSet_check = {}
	closedSet = {}
	g = {}
	for i in range(len(start)):
		g[start[i]] = 0
		openSet.put(start[i],0)
		openSet_check[start[i]]=1
	
	while not openSet.empty():
		currentState = openSet.get()
		closedSet[currentState] = 1
		for nextState in get_successors(currentState):
			if nextState in closedSet:
				continue
			newCost = g[currentState[0]] + get_cost(nextState)
			if nextState not in openSet_check:
				g[nextState] = newCost
				openSet.put(nextState,g[nextState])
				openSet_check[nextState] = 1
				continue
				
			elif newCost >= g[nextState]:
				continue
			
			g[nextState] = newCost
			openSet.put(nextState,g[nextState])
			openSet_check[nextState] = 1
	
	# This writes the cost values onto a file which is accessed by the A-star algorithm
	# for the planning part
	f = open('heuristic.txt','w')
	temp=''
	for i in range(M):
		temp=''
		for j in range(N):
			if j==0:
				temp +=str(g[(i,j)])			
			else:
				temp +=','+str(g[(i,j)]) 
		if i==0:
			f.write(temp)
		else:
			f.write('\n'+temp)
	f.close()
	return g
	
def main():
	global M,N,C
	imarray = parser(sys.argv[1])
	start = []
	rows, cols = np.nonzero(imarray)
	for i in range(len(rows)):
		start.append((rows[i],cols[i]))
	M,N = imarray.shape
	C = np.array(imarray, copy=True)
	im = np.array(imarray, copy=True)
	C[:][:] = 1

	imarray2 = dijkstra(start,C)
	for i in range(M):
		for j in range(N):
			im[i][j] = imarray2[(i,j)]
	
	# Uncomment this to see the distance transform as an image
	'''import matplotlib.pyplot as plt
	imshow(im, cmap = cm.gray)
	plt.show()
	imsave('distanceTransform.png', im)'''
	return im

if __name__ == "__main__": 
	main()
