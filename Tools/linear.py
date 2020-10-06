import numpy as np

def commutator(A,B):
    assert all([a==b for a in np.shape(A) for b in np.shape(B)]),'Matrices of different dimension in commutator.'
    return A.dot(B)-B.dot(A)
    
def trace(A):
    assert all([len(A) == len(A[i]) for i in range(len(A)) ] ), "Trace needs square matrix arg."
    return sum( [ A[i][i] for i in range(len(A)) ] )
    
def isprojector(pi,machine_eps):
    # print("pi=\n",pi)
    # print("pi.pi=\n", pi.dot(pi), "\n")
    diffMat = pi.dot(pi) - pi
    diffList = [entry for row in diffMat for entry in row]
    
    n = len(pi)
    #true if all the entries of pi differed by at most machine_eps from a projector
    return all([entry < n*machine_eps*(2+machine_eps) for entry in diffList])