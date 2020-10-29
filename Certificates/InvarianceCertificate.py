from Certificates.Tools import lin, const, rwalk
import Certificates.Classes.RepClass as rep
import numpy as np
import math

def largestComm_in_Gens(repr,proj):
    #largest commutator with the reps
    assert isinstance(repr,rep.rep_by_generators), "Argument for largestCommutator isnt rep_by_generators"
    return max( (np.linalg.norm(lin.commutator(proj,im), ord='fro') for im in repr.image_list()) )

def largestComm_in_Group(repr,proj,eps):
    assert hasattr(repr,'density'), "Representation has no specified density of generators."
    assert hasattr(repr,'q'), "Representation has no specified q-boundedness."
    
    delta = repr.density[0]
    k = repr.density[1]
    q = repr.q
    n = repr.dimension
    
    partialResult = k*largestComm_in_Gens(repr,proj) 
    partialResult+= 2*k*n*eps*(n*eps+1)
    partialResult+= 2*q*delta*math.exp(q*delta)
    
    return partialResult
    

def quality(repr,proj,eps):
    n = repr.dimension
    C = largestComm_in_Group(repr,proj,eps)+ 2*n*eps
    partialResult = C * (1-C)**(-1)
    partialResult*= math.sqrt(round(lin.trace(proj).real))
    partialResult*= math.pi * math.sqrt(2**(-1))
    return partialResult
    
def inv_cert(repr,proj,epsilon):
    #invariance certificate: is proj close to being invariant in Frob norm?
    
    eps = 2**(-52) #eps=machine epsilon = largest gap in [1,2) between floats (here use double precision).
    assert isinstance(repr,rep.rep_by_generators), "Representation input is not a rep_by_generators object."
    
    return quality(repr,proj,eps) <= epsilon
    
    
    
    
    