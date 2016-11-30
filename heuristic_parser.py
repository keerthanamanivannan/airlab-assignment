#!/usr/bin/env python
import IPython
def heuristic(filename):
	#filename = 'heuristic.txt'
	with open(filename) as f:
		data = f.readlines()

	l, H = [], []
	for n, line in enumerate(data, 1):
		l.append(line.rstrip())

	for i in range(len(l)):	
		H.append(l[i].split(","))
		H[i] = map(int, H[i])
	return H
