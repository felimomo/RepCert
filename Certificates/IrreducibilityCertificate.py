import numpy as np
import math
import random
from Certificates.Tools import lin, const, rwalk
from Certificates.Classes import RepClass as rep

def restrict_to_subrep(repr,basis):
    # restricts repr to a subrepresentation on the space spanned
    # by basis.

    new_ims = [lin.restrict(im,basis) for im in repr.image_list()] # new rep images of generators
    dim = len(basis) # new dimension
    new_repr = rep.rep_by_generators(dim, repr.generatorList, new_ims, density = repr.density, q = repr.q)
    return new_repr
    
def irr_cert(repr,basis,t,epsilon,error_p):
    # irreducibility certificate for random walks of length 2t and false-positive
    # rate of error_p. span(basis) is invariant with precision epsilon.
    
    # restrict to subspace for random walks
    subrep = restrict_to_subrep(repr, basis)
    
    # parameters and constants:
    dim = len(basis)
    m = rwalk.number_samples(subrep,dim,epsilon,error_p,t)
    et = const.et(subrep,epsilon,t,dim)
    dt = const.dt(subrep,epsilon,t)
    aux = dim**2+dt
    aux*= 2*math.log(error_p**(-1))
    
    if et >=2 or m <= aux:
        # the condition for m should be trivially satisfied right now, but keep it in case
        # I use a non-predetermined value of m.
        # 
        # If et >=2, then theta >=1 and so E will never be < 2(1-theta) =< 0.
        return False 

    if dim==1:
        return True
    
    theta = math.sqrt(aux * (m*(2-et))**(-1))
    E = et + rwalk.repRandWalkEstimator(subrep,m,t)
    if E < 2*(1-theta):
        return True
    return False
    
# Old certificate which used the projector onto the subrep:
    
# def irr_cert(repr,proj,t,epsilon,error_p):
#     m = rwalk.number_samples(repr,proj,epsilon,error_p,t)
#     et = const.et(repr,epsilon,t,proj)
#     dt = const.dt(repr,epsilon,t)
#     dim = int(np.trace(proj).real)
#     aux = dim**2+dt
#     aux*= 2*math.log(error_p**(-1))
# 
#     if et >=2 or m <= aux:
#         return False 
# 
#     if dim==1:
#         return True
# 
#     theta = math.sqrt(aux * (m*(2-et))**(-1))
#     E = et + rwalk.repRandWalkEstimator(repr,proj,m,t)
#     if E < 2*(1-theta):
#         return True
#     return False
    
    
    
    
        