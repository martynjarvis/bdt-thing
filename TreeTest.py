from bdtpy.tree import Tree
import numpy as np
from math import pi
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#import random

dt = Tree()

def f(x,y):
    return dt.classify(np.array((x,y)))

samples = 5000

x1 = np.random.normal(1, 2, samples).reshape(-1,1)
y1 = np.random.normal(1, 2, samples).reshape(-1,1)
signalSample     = np.hstack((x1,y1))

x2 = np.random.normal(-1, 2, samples).reshape(-1,1)
y2 = np.random.normal(-1, 2, samples).reshape(-1,1)
backgroundSample     = np.hstack((x2,y2))

dt.load(signalSample,backgroundSample)
dt.build()

delta = 0.025
x = y = np.arange(-3.0, 3.0, delta)
X, Y = np.meshgrid(x, y)

vecF = np.vectorize(f)

Z = vecF(X,Y)

im = plt.imshow(Z,origin='lower', cmap='bone',extent=[-3,3,-3,3])
# interpolation='bilinear',
plt.colorbar(shrink=.92)
plt.show()
