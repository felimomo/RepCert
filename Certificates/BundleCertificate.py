from Certificates import IrreducibilityCertificate as irr
from Certificates import InvarianceCertificate as inv
from Certificates.Tools import rwalk
import math


def best_invariance_certificate(repr,proj):
    # largest_exponent = int(input("Largest epsilon = 10^(-x), (x int > 0), x = "))
    # smallest_exponent = int(input("Smallest epsilon = 10^(-x), (x int > 0), x = "))
    largest_exponent = 1
    smallest_exponent = 15
    epsilon = 10**(-largest_exponent)
    if not inv.inv_cert(repr,proj,epsilon):
        return 1
    for x in range(largest_exponent+1,smallest_exponent+1):
        if not inv.inv_cert(repr,proj,epsilon):
            return epsilon
        epsilon = 10**(-x)
    return 10**(-smallest_exponent)
    
def minimum_t(repr):
    t_min = 0.5 * math.log(repr.dimension-1) 
    t_min*= ( -math.log(1-repr.density[1]**(-2) * repr.nGens**(-1)) )**(-1) #minimum t from converse result
    t_min = int(t_min)
    return t_min
    
def subrep_tester(repr,proj,t_surplus,error_p,prnt=False):
    # error_p = eval(input("error p threshold = "))
    # t_max = int(eval(input("use random walks of length (t) at most = ")))
    # prnt : if true, then print the minimal epsilon of the invariance certificate
    
    t_min = minimum_t(repr)
    t_max = t_min + t_surplus #just some arbitrary extra amount, to be benchmarked
    
    #Invariance test:
    epsilon = best_invariance_certificate(repr,proj)
    if prnt:
        print("Invariant at precision ",epsilon)
        print("Minimal rand walk length = ", 2*t_min)
        nsamp = rwalk.number_samples(repr,proj,epsilon,error_p,t_max)
        print("Max number of samples required for irreducibility: ", nsamp)
        
    if epsilon==1:
        return False
    
    #Irreducibility test:
    for t in range(t_min,t_max+1):
        if irr.irr_cert(repr,proj,t,epsilon,error_p):
            # print("Irreducible!\n")
            return True
    # print("Dont know if irreducible!\n")
    return False
    
    
 
    
    
    
    
    
    
    
    
    
    