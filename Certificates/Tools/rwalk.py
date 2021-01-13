import numpy as np
import random
import math
from Certificates.Tools import const
from Certificates.Tools import lin

def repRandWalk(repr,t):
    # Calculates |tr( ... )|^2 for '...' = random walk in the representation repr.
    # Length of random walk = 2t.
    #
    w = np.eye(repr.dimension).astype(complex)
    for i in range(t):
        w *= np.asmatrix(random.choice(repr.image_list()))
    return abs(np.trace(w))**2
    
def repRandWalkEstimator(repr,m,t):
    # Estimates the character length E_g{{ |tr( rho_g)|^2 }} using m samples of random
    # walks of length 2t.
    # 
    est = (repRandWalk(repr,t) * m**(-1) for i in range(m))
    return sum(est)
    
#
# Random walk parameter values m and t:
#
    
def number_samples(repr,dim,epsilon,error_p,t):
    
    minimum = 2*math.log(error_p**(-1))
    dt = const.dt(repr,epsilon,2*t)
    minimum*= dim**2 + dt # Minimum m such that irr_cert doesnt abort
    return 16*int(extra_factor*minimum) # extra 16 factor for false positives (Prop. 5)
    
def minimum_t(repr,setting='promise'):
    if setting=='promise':
        return 2+int(math.log(repr.dimension,2))
        
        
    # else, setting == 'fixed' and I use a cheap trick:
    
    if hasattr(repr, 'order') or repr.Lie:
        # in practice the above value of t_min seems too large for small finite groups.
        # replace it by an ad-hoc value of t_min here, given by twice the Cayley diam.
        # return 2*repr.density[1]
        #
        # Also use it for Lie groups, what the hell.
        
        # nah, let's try something outrageous
        return math.ceil(0.5*repr.density[1])
        
    # The true bound for 'fixed' setting, which gets horrible quickly
    
    t_min = 0.5 * math.log(repr.dimension-1) 
    t_min*= ( -math.log(1-repr.density[1]**(-2) * repr.nGens**(-1)) )**(-1) #minimum t from converse result
    t_min = int(t_min)
    return t_min
    
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
    
