from Certificates import IrreducibilityCertificate as irr
from Certificates import InvarianceCertificate as inv
from Certificates.Tools import rwalk
import math
import numpy as np


def best_invariance_certificate(repr,proj):
    # largest_exponent = int(input("Largest epsilon = 10^(-x), (x int > 0), x = "))
    # smallest_exponent = int(input("Smallest epsilon = 10^(-x), (x int > 0), x = "))
    largest_exponent = 1
    smallest_exponent = 25
    epsilon = 10**(-largest_exponent)
    if not inv.inv_cert(repr,proj,epsilon):
        return 1
    for x in range(largest_exponent+1,smallest_exponent+1):
        if not inv.inv_cert(repr,proj,epsilon):
            return epsilon
        epsilon = 10**(-x)
    return epsilon
    
def minimum_t(repr):
    t_min = 0.5 * math.log(repr.dimension-1) 
    t_min*= ( -math.log(1-repr.density[1]**(-2) * repr.nGens**(-1)) )**(-1) #minimum t from converse result
    t_min = int(t_min)
    if hasattr(repr, 'order'):
        # in practice the above value of t_min seems too large for small finite groups.
        # replace it by an ad-hoc value of t_min here, given by twice the Cayley diam.
        t_min = 2*repr.density[1]
    return t_min
    
def subrep_tester(repr,proj,t_surplus,error_p,prnt=False):
    
    if repr.dimension==1:
        return True
    
    t_min = minimum_t(repr)
    t_max = t_min + t_surplus
    
    #Invariance test:
    epsilon = best_invariance_certificate(repr,proj)
    if prnt:
        print("Invariant at precision ",epsilon)
        print("Minimal rand walk length = ", 2*t_min)
        print("Max number of samples required for irreducibility: ", 
                rwalk.number_samples(repr,proj,epsilon,error_p,t_max)
                )
        print("Dimension of irrep being tested = ", int(np.trace(proj).real))
        
    if epsilon==1:
        return False
    
    #Irreducibility test:
    for t in range(t_min,t_max+1):
        if irr.irr_cert(repr,proj,t,epsilon,error_p):
            return True
    return False
    
    
 
    
    
    
    
    
    
    
    
    
    