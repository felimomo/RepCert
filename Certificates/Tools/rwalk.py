import numpy as np
import random
import math
from Certificates.Tools import const
from Certificates.Tools import lin

def repRandWalk(repr,t):
    w = np.eye(repr.dimension).astype(complex)
    for i in range(t):
        w *= np.asmatrix(random.choice(repr.image_list()))
    return abs(np.trace(w))**2
    
def repRandWalkEstimator(repr,m,t):
    # estimator for random walk of length 2t
    # print("random walk length = ",2*t)
    est = (repRandWalk(repr,t) * m**(-1) for i in range(m))
    return sum(est)
    
def number_samples(repr,dim,epsilon,error_p,t,extra_factor=4):
    minimum = 2*math.log(error_p**(-1))
    dt = const.dt(repr,epsilon,2*t)
    minimum*= dim**2 + dt #Minimum m such that irr_cert doesnt abort
    return int(extra_factor*minimum)
    
# Old functions that used a projector as an input:

# def repRandWalk(repr,t,proj):
#     P = np.asmatrix(proj)
#     w = np.eye(repr.dimension).astype(complex)
#     for i in range(t):
#         w *= P*np.asmatrix(random.choice(repr.image_list()))*P.H
#     return abs(np.trace(w))**2

# def repRandWalkEstimator(repr,proj,m,t):
#     # estimator for random walk of length 2t
#     # print("random walk length = ",2*t)
#     est = (repRandWalk(repr,t,proj) * m**(-1) for i in range(m))
#     return sum(est)
    
