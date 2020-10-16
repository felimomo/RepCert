import IrreducibilityCertificate as irr
import InvarianceCertificate as inv

def best_invariance_certificate(repr,proj):
    largest_epsilon = int(input("Largest epsilon = 10^(-x), (x int > 0), x = "))
    smallest_epsilon = int(input("Smallest epsilon = 10^(-x), (x int > 0), x = "))
    epsilon = 10**(-largest_epsilon)
    if not inv.inv_cert(repr,proj,epsilon):
        return 1
    for x in range(largest_epsilon+1,smallest_epsilon+1):
        if not inv.inv_cert(repr,proj,epsilon):
            return epsilon
        epsilon = 10**(-x)
    return 10**(-smallest_epsilon)
    
def subrep_tester(repr,proj):
    error_p = eval(input("error p threshold = "))
    t_max = int(eval(input("use random walks of length (t) at most = ")))
    
    #Invariance test:
    epsilon = best_invariance_certificate(repr,proj)
    if epsilon==1:
        print("Not invariant!\n")
        return False
    print("Invariant with precision "+str(epsilon)+"\n")
    
    #Irreducibility test:
    for t in range(1,t_max+1):
        if irr.irr_cert(repr,proj,t,epsilon,error_p):
            print("Irreducible!\n")
            return True
    print("Dont know if irreducible!\n")
    return False
    
    
    
    
    
    
    
    
    
    
    
    
    