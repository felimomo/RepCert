from Certificates import IrreducibilityCertificate as irr
from Certificates import InvarianceCertificate as inv
from Certificates.Tools import rwalk, lin
import math
import numpy as np


def best_invariance_certificate(repr,basis):

    # Create projector to feed the invariance certificate
    proj = lin.toproj(basis)
    
    # prepare to sweep over epsilon the invariance certificate
    largest_exponent = 1
    smallest_exponent = 25
    epsilon = 10**(-largest_exponent)
    
    if not inv.inv_cert(repr,proj,epsilon):
        return 1
        
    for x in range(largest_exponent+1,smallest_exponent+1):
        if not inv.inv_cert(repr,proj,10**(-x)):
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
        # t_min = 2*repr.density[1]
        
        # nah, let's try something outrageous
        t_min = math.ceil(0.5*repr.density[1])
    return t_min
    
def subrep_tester(repr,basis,t_surplus,error_p,prnt=False):
    # Run certificate with rand walks with values of t from minimum_t(repr)
    # to minimum_t(repr)+t_surplus.
    # 
    # If prnt=True, then print a bunch of relevant parameters.
    
    if repr.dimension==1:
        return True
    
    t_min = minimum_t(repr)
    t_max = int(t_min + t_surplus)
    
    #Invariance test:
    epsilon = best_invariance_certificate(repr,basis)
    if prnt:
        dim = len(basis)
        print("Invariant at precision ",epsilon)
        print("Minimal rand walk length = ", 2*t_min)
        print("Max number of samples required for irreducibility: ", rwalk.number_samples(repr,len(basis),epsilon,error_p,t_max))
        print("Dimension of irrep being tested = ", dim)
        
    if epsilon==1:
        return False
    
    #Irreducibility test:
    for t in range(t_min,t_max+1):
        if irr.irr_cert(repr,basis,t,epsilon,error_p):
            return True
    return False
    
    
 
    
    
    
    
    
    
    
    
    
    