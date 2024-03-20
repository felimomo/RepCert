import numpy as np
import math
import random
from repcert.rwalk import set_t, number_samples, repRandWalkEstimator
import replab.tools.const
# from Certificates.Tools import lin, const, rwalk
# from Certificates.Classes import RepClass as rep
    
def irr_cert(repr,epsilon,thresh,conf,setting='promise'):
    # Input:    repr    = a representation (repcert.classes.rep_by_generators.repByGenerators) suspected to be irreducible,
    #           epsilon = invariance precision
    #           thresh  = threshold probability of false positive
    #           conf    = confidence parameter
    #           setting = 'promise' or 'fixed' (promise = generator set is Haar-sampled and symmetrized)
    #
    # Output:   True/False. 
    #           If True, repr is irreducible with probability at least thresh.
    #           If False, repr could be either.

    # parameters and constants:
    dim = repr.dimension
    if dim==1:
        return True
    
    # Random walk parameters #
    t_surplus = 10 # for now ad-hoc -- only relevant for setting = 'fixed'
    t = rwalk.set_t(repr,setting,t_surplus)
    m = rwalk.number_samples(repr,dim,epsilon,thresh,t,conf)
    #
    
    # other constants $
    et = repcert.tools.const.et(repr,epsilon,t,dim)
    dt = repcert.tools.const.dt(repr,epsilon,t)
    aux = dim**2+dt
    aux*= 2*math.log(thresh**(-1))
    #
    
    if et >=2 or m <= aux:
        # the condition for m should be trivially satisfied right now, but keep it in case
        # I use a non-predetermined value of m later.
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
    

    
    
    
    
        