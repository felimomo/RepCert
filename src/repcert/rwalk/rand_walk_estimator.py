import numpy as np
import random
import math

def repRandWalk(repr,t):
    # Calculates |tr( ... )|^2 for '...' = random walk in the representation repr.
    # Length of random walk = 2t.
    #
    w = np.eye(repr.dimension).astype(complex)
    for i in range(t):
        w *= np.asmatrix(random.choice(repr.image_list()))
    return abs(np.trace(w))**2

def randWalkEstimator(repr,m,t):
    # Estimates the character length E_g{{ |tr( rho_g)|^2 }} using m samples of random
    # walks of length 2t.
    # 
    est = (repRandWalk(repr,t) * m**(-1) for i in range(m))
    return sum(est)