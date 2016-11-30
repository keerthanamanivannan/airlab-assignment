#!/usr/bin/env python
"""@package docstring
Documentation for this module.
This code implements the A-Star algorithm to minimize the total cost from the obstacle
traveled by the robot
"""
import math
import sys
import numpy as np
from dijkstra import *
from pylab import *
from heuristic_parser import heuristic
from parser import parser
import matplotlib.pyplot as plt
from PriorityQueue import PriorityQueue

def get_cost(C,state):
	"""Input: Cost map and State 
   	Output: The Cost of the queried state
   	This function returns Cost of each cell in the input image map 
   	"""
	(x,y) = state
	return 255-C[x][y]

def get_heuristic(state1, state2):
	"""Input: Initial State and Goal State 
	Output: The Heuristic of traversing from state1 to state2
   	This function uses the Manhattan distance as heuristic
    	"""
	(x1,y1) = state1
	(x2,y2) = state2
	return math.fabs((x1-x2) + (y1-y2))

def inBounds(state):
	"""Input: State 
   	Output: Bool value whether the state is in bounds or not
   	This function returns whether the queried state is in bounds of the image or not
    	"""
	(x,y)= state
	return 0<=x<M and 0<=y<N

def get_successors(state):
	"""Input: State 
   	Output: Successors of the queried state
   	This function assumes a four connected gridworld and outputs the successors of the current state
    	"""
	(x,y) = state
	successors = [(x,y),(x+1,y),(x,y-1),(x-1,y),(x,y+1)]
	successors = filter(inBounds,successors)
	return successors

def reconstruct_path(plan,currentState):
	"""Input: plan 
   	Output: Bool value whether the state is in bounds or not
   	This function returns whether the queried state is in bounds of the image or not
    	"""
	totalPath = [currentState]
	while(1):
		try:	
			currentState = plan[currentState]
			totalPath.append(currentState)
		except:
			break
	return totalPath

def visualize(path,C,im):
	"""Input: plan path, Cost map and the original map 
   	Output: Plot the plan path on the original map
   	This function is used for visualization
    	"""
	plt.imshow(im)
	for i in range(len(path)):
		plt.scatter(x=path[i][1],y = path[i][0],c='b')
	plt.show()

def get_totalCost(plan,C):
	"""Input: plan, Cost map
	   Output: Sums up the total cost of the planned path
	"""
	totalCost = 0
	for i in range(len(plan)):
		(x,y) = plan[i]
		totalCost = totalCost + C[x][y]
	print "The total Path length is:" + str(totalCost)

def Astar(start,goal,C,im):
	"""Input: Start state, Goal State, Cost map and original map
	Output: Bool value False after completion of the algorithm
	This function performs the A-Star algorithm to optimize wrt to the cost of near each obstacle
	"""
	openSet = PriorityQueue()
	openSet.put(start,0)
	openSet_check = {}
	openSet_check[start]=1
	closedSet = {}
	plan = {}
	g = {}
	g[start] = 0
	f = {}
	j=0
	f[start] = get_heuristic(start, goal)
	while not openSet.empty():
		currentState,fpop = openSet.get()
		if currentState == goal:
			print "Path found!"
			path = reconstruct_path(plan,currentState)
			path.reverse()			
			get_totalCost(path,C)
			visualize(path,C,im)
			#for i in range(len(path)):
			#	print path[i]
			break

		closedSet[currentState] = 1
		for nextState in get_successors(currentState):
			j=j+1
			if nextState in closedSet:
				continue

			newCost = g[currentState] + get_cost(C,nextState)
			if nextState not in openSet_check:
				plan[nextState] = currentState
				g[nextState] = newCost
				f[nextState] = g[(nextState)] + get_heuristic(currentState,nextState)

				openSet.put(nextState,f[nextState])
				openSet_check[nextState] = 1
				continue

			elif newCost >= g[nextState]:
				openSet_check[nextState] = 1
				continue
			
			plan[nextState] = currentState
			g[nextState] = newCost
			f[nextState] = g[(nextState)] + get_heuristic(currentState,nextState)

			openSet.put(nextState, f[nextState])
			openSet_check[nextState] = 1
	
	return False

def main():
	im = parser(sys.argv[1])
	goal = (1035,910) # because the x,y pixel is x-column and y-row 
	start = (144,144)
	global M,N
	M,N = im.shape
	#C = np.array(imarray, copy=True)
	C = np.asarray(heuristic(sys.argv[2]))
	Astar(start,goal,C,im)

if __name__ == "__main__": 
	main()
