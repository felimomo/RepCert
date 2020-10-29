import numpy as np
import math
import random
from Certificates.Tools import lin, const, rwalk
    
def irr_cert(repr,proj,t,epsilon,error_p):
    m = rwalk.number_samples(repr,proj,epsilon,error_p,t)
    et = const.et(repr,epsilon,t,proj)
    dt = const.dt(repr,epsilon,t)
    dim = int(np.trace(proj).real)
    aux = dim**2+dt
    aux*= 2*math.log(error_p**(-1))
    
    if et >=2 or m <= aux:
        return False 

    if dim==1:
        return True
    
    theta = math.sqrt(aux * (m*(2-et))**(-1))
    E = et + rwalk.repRandWalkEstimator(repr,proj,m,t)
    if E < 2*(1-theta):
        return True
    return False
    
    
    
    
        