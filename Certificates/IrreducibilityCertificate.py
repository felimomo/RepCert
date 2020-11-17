import numpy as np
import math
import random
from Certificates.Tools import lin, const, rwalk
from Certificates.Classes import RepClass as rep
    
def irr_cert(repr,t,epsilon,error_p):
    # Input:    repr    = a representation (RepClass.rep_by_generators) suspected to be irreducible,
    #           t       = half-length of random walk
    #           epsilon = invariance precision
    #           error_p = threshold probability of false positive
    #
    # Output:   True/False. 
    #           If True, repr is irreducible with probability at least error_p.
    #           If False, repr could be either.

    # parameters and constants:
    dim = repr.dimension
    if dim==1:
        return True
    m = rwalk.number_samples(repr,dim,epsilon,error_p,t)
    et = const.et(repr,epsilon,t,dim)
    dt = const.dt(repr,epsilon,t)
    aux = dim**2+dt
    aux*= 2*math.log(error_p**(-1))
    
    if et >=2 or m <= aux:
        # the condition for m should be trivially satisfied right now, but keep it in case
        # I use a non-predetermined value of m.
        # 
        # If et >=2, then theta >=1 and so E will never be < 2(1-theta) =< 0.
        return False 
    
    # Character length estimation:
    theta = math.sqrt(aux * (m*(2-et))**(-1))
    E = et + rwalk.repRandWalkEstimator(repr,m,t)
    
    # Irreducibility condition:
    if E < 2*(1-theta):
        return True
    return False
    

    
    
    
    
        