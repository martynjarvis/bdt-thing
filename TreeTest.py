from bdtpy.tree import Tree
import numpy as np
from math import pi
#import random

dt = Tree()

a = np.random.normal(1, 1, 10).reshape(-1,1)
b = np.random.normal(1, 1.5, 10).reshape(-1,1)
signalSample     = np.hstack((a,b))

c = np.random.normal(0, 1, 100).reshape(-1,1)
d = np.random.normal(0, 1.5, 100).reshape(-1,1)
backgroundSample     = np.hstack((c,d))

dt.load(signalSample,backgroundSample)
dt.build()

test = np.array((1.,1.))
print dt.classify(test)
