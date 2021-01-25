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
    
def number_samples(repr,dim,epsilon,error_p,t,conf=None):
    # dim = dimension of subrepresentation being tested
    # error_p = threshold false positive rate
    # conf = confidence parameter (approximate false negative rate)
    # epsilon = invariance certificate precision
    # 2t = length of random walks
    #
    # output = number of random walks sampled
    
    if conf is None:
        # if no confidence parameter is provided, set it to 2*error_p
        conf = 2*error_p
    
    dimfactor = 2*dim**2
    log1 = math.log( error_p**(-1) )
    log2 = math.log( (conf-error_p)**(-1) )
    otherfactor = max(math.ceil(log1),8*math.ceil(log2))
    
    return dimfactor*otherfactor
    # 
    # minimum = 2*math.log(error_p**(-1))
    # dt = const.dt(repr,epsilon,2*t)
    # minimum*= dim**2 + dt # Minimum m such that irr_cert doesnt abort
    # return 16*int(extra_factor*minimum) # extra 16 factor for false positives (Prop. 5)
    
def set_t(repr,setting='promise',t_surplus=0):
    # output = 1/2 random walk length
    #
    # setting: 'promise' (Haar random) vs 'fixed' generator set
    # t_surplus: in the case of setting = 'fixed', output = output + t_surplus
    #
    if setting=='promise':
        return 2+math.ceil(math.log(repr.dimension,2))
        
        
    # else, setting == 'fixed' and I use a cheap trick:
    
    if hasattr(repr, 'order') or repr.Lie:
        # in practice the value of t_min below seems too large for practical
        # purposes. Use k/2 + surplus
        
        return math.ceil(0.5*repr.density[1])+t_surplus
        
    # The true bound for 'fixed' setting, which gets horrible quickly
    
    t = 0.5 * math.log(repr.dimension-1) 
    t*= ( -math.log(1-repr.density[1]**(-2) * repr.nGens**(-1)) )**(-1) #minimum t from converse result
    t = int(t)
    return t
    

    
