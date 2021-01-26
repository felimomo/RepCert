import numpy as np
import math
from Certificates.Tools import lin, const, rwalk, checks
import Certificates.Classes.RepClass as rep

def inv_cert(repr,proj,epsilon,error_p=10**(-7),fl=2**(-52),setting='promise'):
    #
    # Two options for setting: 'promise' or 'fixed'. Will toggle
    # between Alg. XX and Alg. YY in paper arXiv:------
    #
    # repr = representation object, proj = projector to be tested,
    # epsilon = precision of certificate (eps-close to an invar. proj.)
    # error_p = threshhold prob of false positive (only relevant 
    # for setting='promise'.)
    # fl = precision to which the rep images and proj are defined (default
    # is fl = double precision)
    #
    if setting=='promise':
        return promise_inv(repr,proj,epsilon,error_p,fl)
    if setting=='fixed':
        return fixed_inv(repr,proj,epsilon)
    else:
        print("Invalid setting for invariance certificate.\n")
        return 1
    
    

# Promise setting (probabilistic)
#
# For generator set S with promise, S was obtained in the following way:
#   1. Sample 12 ceiling[ ln(2/error_p) + 2 ln(dim) ] many elements gi Haar randomly 
#   2. Set S = { gi, gi^-1 }
#

def avg_comm(repr,proj):
    comms = (lin.commutator(im,proj) for im in repr.image_list())
    c = np.linalg.norm(sum(comms),ord=2)/len(repr.image_list())
    return c
    
def promise_inv(repr,proj,epsilon,error_p,fl):
    #
    # invariance certificate in the 'promise' setting.
    epsprime = epsilon/(2*math.sqrt(2.*math.ceil(lin.trace(proj).real)))
    c = avg_comm(repr,proj)
    n = repr.dimension
    f_err = 8*n*fl + 6*(n*fl)**2 + 2*(n*fl)**3
    print("c = ", c)
    print("f_err = ",f_err)
    # projnorm = np.linalg.norm(proj)
    # numerator = math.log(2)*projnorm
    # denominator = c + 4*repr.dimension*fl + 4*(repr.dimension*fl)**2
    # k = math.ceil(math.log(numerator/denominator,2))
    if 2*c + f_err <= epsprime:
        return True
    return False




# Deterministic certificate
#
# For FIXED generator set S, with parameters k, delta, q:
#   - rho is q-bounded unitary rep
#   - S is (delta,k)-dense in G
#

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
    
def fixed_inv(repr,proj,epsilon):
    #invariance certificate: is proj close to being invariant in Frob norm?
    
    eps = 2**(-52) #eps=machine epsilon = largest gap in [1,2) between floats (here use double precision).
    assert isinstance(repr,rep.rep_by_generators), "Representation input is not a rep_by_generators object."
    
    return quality(repr,proj,eps) <= epsilon
    
    
    
    
    