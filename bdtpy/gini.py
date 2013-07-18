import numpy as np

def gini(s,b):
    if s<=0 : return 0
    elif b<=0 : return 0
    return 2*float(s*b)/((s+b)*(s+b))
    # RuntimeWarning: overflow encountered in long_scalars when s+b>50000

def weightedGini(s,b):
    return (s+b)*gini(s,b)

vecGini = np.vectorize(gini)
vecWeightedGini = np.vectorize(weightedGini)