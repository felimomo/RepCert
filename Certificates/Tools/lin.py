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

def single_row_mat(vec):
    return np.array([[comp for comp in vec]])

def ketbra(vec):
    # takes a vector and produces a projector onto its span
    mat_v = single_row_mat(vec)
    mat_v = np.linalg.norm(mat_v)**(-1) * mat_v # normalize
    return mat_v.conjugate().transpose().dot(mat_v)   # column*row = | > < |
    
def braket(v1,v2):
    mat_v1 = single_row_mat(v1).conjugate()
    mat_v2 = single_row_mat(v2).transpose()
    return mat_v1.dot(mat_v2)[0][0]

def check_ortho(v1,v2,thr=10**(-12)):
    # checks whether v1 is orthogonal to v2
    return abs(braket(v1,v2)) < thr
    
def check_orthonorm_basis(basis,thr=10**(-12)):
    # checks whether basis is orthonormal
    orthogonality = all((check_ortho(basis[i],basis[j]) for i in range(len(basis)) for j in range(i)))
    normalization = all((1-thr < abs(braket(basis_elem,basis_elem)) < 1+thr for basis_elem in basis))
    # abs( ... ) needed to force the data type to be float, but 
    # also be able to catch if there would be large imaginary
    # part for whatever reason.
    
    return orthogonality# and normalization 
                

def toproj(basis):
    # takes basis = [ basis element 1, basis element 2, ... ] and
    # creates a projector onto their span (assuming they're orthogonal).
    assert all((len(elem)==len(basis[0]) for elem in basis)), "All basis elements must have same dimension."
    assert check_orthonorm_basis(basis), "Basis is not orthogonal."
    
    return sum((ketbra(elem) for elem in basis))
    
    
def as_lincomb(vec, basis, thr=10**(-12)):
    # Decomposes vector as linear combination of basis elements.
    # Assumption is that basis is orthogonal and vec lies in
    # the span of the basis (up to numerical errors).
    #
    # If vector is orthogonal, then returns list of 0's
    #
    # Returns coefficients [c_i] such that sum_i c_i basis[i] = vec
    coeff = [braket(basis_elem, vec) for basis_elem in basis]
    
    assert check_orthonorm_basis(basis), "Basis is not orthonormal."
    return coeff
    
def restrict(mat,basis):
    #restrict matrix mat to the subspace spanned by basis
    return np.array([as_lincomb(mat.dot(basis_elem),basis) for basis_elem in basis]).transpose()    

    

    
    
    