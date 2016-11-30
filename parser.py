#!/usr/bin/env python
import Image
import numpy
import IPython
import matplotlib.pyplot as plt
from pylab import *
def parser(filename):
	#filename = '4_1_map.png'
	im1 = Image.open(filename)
	imarray = numpy.array(im1)
	#imshow(imarray, cmap = cm.gray)
	#plt.show()
	return imarray

