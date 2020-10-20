import Tools as t
import numpy as np
import math

def largestComm_in_Gens(repr,proj):
    #largest commutator with the reps
    assert isinstance(repr,t.RepClass.rep_by_generators), "Argument for largestCommutator isnt rep_by_generators"
    return max( (np.linalg.norm(t.linear.commutator(proj,im), ord='fro') for im in repr.image_list()) )

def largestComm_in_Group(repr,proj,eps):
    assert hasattr(repr,'density'), "Representation has no specified density of generators."
    assert hasattr(repr,'q'), "Representation has no specified q-boundedness."
    
    delta = repr.density[0]
    k = repr.density[1]
    q = repr.q
    n = repr.dimension
    
    partialResult = k*largestComm_in_Gens(repr,proj) 
    partialResult+= 2*k*n*eps*(n*eps+1)
    partialResult+= q*delta*math.exp(q*delta)
    
    return partialResult
    

def quality(repr,proj,eps):
    #eps=machine epsilon.
    n = repr.dimension
    C = largestComm_in_Group(repr,proj,eps)+ 2*n*eps
    partialResult = C * (1-C)**(-1)
    partialResult*= math.sqrt(round(t.linear.trace(proj).real))
    partialResult*= math.pi * math.sqrt(2**(-1))
    return partialResult
    
def inv_cert(repr,proj,epsilon):
    #eps=machine epsilon = largest gap in [1,2) between floats (2^-52 for double precision).
    eps = 2**(-52)
    #returns true if proj is epsilon-close to invariant-projector in frob norm
    # assert t.linear.isprojector(proj,eps), "Projector input is not close to a projector."
    assert isinstance(repr,t.RepClass.rep_by_generators), "Representation input is not a rep_by_generators object."
    
    return quality(repr,proj,eps) <= epsilon
    
    
    
    
    