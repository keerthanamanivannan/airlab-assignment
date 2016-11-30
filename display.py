import Image
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from pylab import *

im1 = Image.open("4_1_map.png")
im1 = np.asarray(im1)
im2 = ndimage.distance_transform_edt(im1==0)
imshow(im2, cmap = cm.gray)
plt.show()
