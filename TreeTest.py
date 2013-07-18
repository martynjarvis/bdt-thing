from bdtpy.tree import Tree
import numpy as np
from math import pi
#import random

dt = Tree()

samples = 50000

a = np.random.normal(1, 1, samples).reshape(-1,1)
b = np.random.normal(1, 1.5, samples).reshape(-1,1)
signalSample     = np.hstack((a,b))

c = np.random.normal(0, 1, samples).reshape(-1,1)
d = np.random.normal(0, 1.5, samples).reshape(-1,1)
backgroundSample     = np.hstack((c,d))

dt.load(signalSample,backgroundSample)
dt.build()

dt.draw()
test_sig = np.array((1.,1.))
print dt.classify(test_sig)
test_bkg = np.array((0.,0.))
print dt.classify(test_bkg)
