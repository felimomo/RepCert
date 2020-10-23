import IrreducibilityCertificate as irr
import InvarianceCertificate as inv
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
    
def subrep_tester(repr,proj,t_surplus,error_p):
    # error_p = eval(input("error p threshold = "))
    # t_max = int(eval(input("use random walks of length (t) at most = ")))
    
    t_min = minimum_t(repr)
    t_max = t_min + 10 #just some arbitrary extra amount, to be benchmarked
    
    #Invariance test:
    epsilon = best_invariance_certificate(repr,proj)
    if epsilon==1:
        # print("Not invariant!\n")
        return False
    # print("       Invariant with precision "+str(epsilon))
    
    #Irreducibility test:
    for t in range(t_min,t_max+1):
        if irr.irr_cert(repr,proj,t,epsilon,error_p):
            # print("Irreducible!\n")
            return True
    # print("Dont know if irreducible!\n")
    return False
    
    
 
    
    
    
    
    
    
    
    
    
    