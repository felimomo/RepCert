import numpy as np
import random
import math
import Certificates.Tools.const as const

def repRandWalk(repr,t,proj):
    P = np.asmatrix(proj)
    w = np.eye(repr.dimension).astype(complex)
    for i in range(t):
        w *= P*np.asmatrix(random.choice(repr.image_list()))*P.H
    return w

def repRandWalkEstimator(repr,proj,m,t):
    #estimator for random walk of length 2t
    # print("random walk length = ",2*t)
    est = 0
    for i in range(m):
        est += abs(np.trace(repRandWalk(repr,t,proj)))**2 * m**(-1)
    return est
    
def number_samples(repr,proj,epsilon,error_p,t):
    dim = int(np.trace(proj).real)
    minimum = 2*math.log(error_p**(-1))
    dt = const.dt(repr,epsilon,2*t)
    minimum*= dim**2 + dt #Minimum m such that irr_cert doesnt abort
    extra_factor = 3 #To be sure that we have enough samples
    return int(extra_factor*minimum)+10