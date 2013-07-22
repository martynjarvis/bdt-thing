from bdtpy.bdt import BDT
import numpy as np
from math import pi 
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# BDT example. Two 2d gaussians, signal centred at +1,+1 and background centred at -1,-1

events = 1000

# Create BDT
bdt = BDT()

# create and load training samples
signal = np.random.normal(1, 1.5, 2*events).reshape(-1,2)
background = np.random.normal(-1, 1.5, 2*events).reshape(-1,2)
bdt.load(signal,background)

# Train
bdt.build()

# show plot of BDT output against x,y
delta = 0.05
x = y = np.arange(-3.0, 3.0, delta)
X, Y = np.meshgrid(x, y)

# TODO a vectorised version of the classify fn should be in the BDT class
def f(x,y):
    return bdt.classify(np.array((x,y)))
vecF = np.vectorize(f)

Z = vecF(X,Y)
im = plt.imshow(Z,origin='lower', cmap='bone',extent=[-3,3,-3,3])
plt.colorbar(shrink=.92)
plt.show()


# fig = plt.figure()
# ax = fig.add_subplot(111)

# sig = []
# bkg = []

# for i in range(samples):
#     sig.append(f(x1[i],y1[i]))
#     bkg.append(f(x2[i],y2[i]))

# # for 

# n, bins, patches = ax.hist(sig, 10, normed=1, facecolor='blue', alpha=0.75)
# n, bins, patches = ax.hist(bkg, 10, normed=1, facecolor='red', alpha=0.75)

# plt.show()
