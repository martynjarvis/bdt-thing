from bdtpy.bdt import BDT
import numpy as np
from math import pi 
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

bdt = BDT()

def f(x,y):
    return bdt.classify(np.array((x,y)))
vecF = np.vectorize(f)

samples = 5000

x1 = np.random.normal(1, 2, samples).reshape(-1,1)
y1 = np.random.normal(1, 2, samples).reshape(-1,1)
signalSample     = np.hstack((x1,y1))
x2 = np.random.normal(-1, 2, samples).reshape(-1,1)
y2 = np.random.normal(-1, 2, samples).reshape(-1,1)
backgroundSample     = np.hstack((x2,y2))

bdt.load(signalSample,backgroundSample)
bdt.build()

delta = 0.05
x = y = np.arange(-3.0, 3.0, delta)
X, Y = np.meshgrid(x, y)
Z = vecF(X,Y)

im = plt.imshow(Z,origin='lower', cmap='bone',extent=[-3,3,-3,3])
# interpolation='bilinear',
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
