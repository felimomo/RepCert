from Certificates import IrreducibilityCertificate as irr
from Certificates import InvarianceCertificate as inv
from Certificates.Tools import rwalk, lin
from Certificates.Classes import RepClass as rep
import math
import numpy as np
import itertools as itr

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
    
def restrict_to_subrep(repr,basis):
    # restricts repr to a subrepresentation on the space spanned
    # by basis.

    new_ims = [lin.restrict(im,basis) for im in repr.image_list()] # new rep images of generators
    dim = len(basis) # new dimension
    new_repr = rep.rep_by_generators(dim, repr.generatorList, new_ims, density = repr.density, q = repr.q)
    return new_repr

def subrep_tester(repr,basis,t_surplus,error_p,prnt=False):
    # Run certificate with rand walks with values of t from minimum_t(repr)
    # to minimum_t(repr)+t_surplus.
    # 
    # If prnt=True, then print a bunch of relevant parameters.
    
    if repr.dimension==1:
        return True
        
    t_min = int(rwalk.minimum_t(repr))
    t_max = int(t_min + t_surplus)
    t_range = itr.chain(range(1,5),range(t_min,t_max+1))
    
    # ad-hoc mish-mash for continuous groups to escape the huge t values [not needed right now]


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
        
    subrep = restrict_to_subrep(repr,basis)
    
    #Irreducibility test:
    for t in t_range:
        print(t, end="\r")
        if irr.irr_cert(subrep,t,epsilon,error_p):
            # print("Needed random walk length: ", 2*t)
            return True
    return False
    
    
 
    
    
    
    
    
    
    
    
    
    