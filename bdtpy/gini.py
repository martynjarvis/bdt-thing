import numpy as np
# Ensure that these functions don't overflow 
# TODO rewrite in terms of (s/s+b)

def gini(s,b):
    if s<=0 : return 0
    elif b<=0 : return 0
    return 2*float(s*b)/((s+b)*(s+b))

def weightedGini(s,b):
    return (s+b)*gini(s,b)

vecGini = np.vectorize(gini)
vecWeightedGini = np.vectorize(weightedGini)