import numpy as np
import random as rnd
import cmath
from scipy import linalg


def haar_unitary(dim):
    # sample from the ginibre distribution
    gin = np.random.normal(0, 0.5, (dim, dim)) + 1.j*np.random.normal(0, 0.5, (dim, dim))
    # QR decomposition
    q,r = linalg.qr(gin)
    # Normalising factor to make R' = lamb^* R have positive diagonal
    lamb = np.diag([r[i][i]*abs(r[i][i])**(-1) for i in range(len(r))])
    # Corresponding Q' = Q lamb
    return q.dot(lamb)
    
def diag_noise(dim,noise_level):
    # samples a unitary diagonal matrix, where phases are Gaussian random
    # variables with variance = noise_level
    return np.diag([cmath.exp(2.j*cmath.pi*np.random.normal(0,noise_level)) for i in range(dim)])
    
def unitary_noise(dim,noise_level):
    # Noise model for slightly rotating the basis:
    #
    # - sample diagonal close to 1
    # - rotate it to a random orthonormal basis
    #
    # Gives a random unitary close to the identity in some random direction.
    D = diag_noise(dim,noise_level)
    U = haar_unitary(dim)
    return U.dot(D.dot(U.conjugate().transpose()))
    
def basis_noise(basis,noise_level):
    # Takes basis and produces a slightly rotated basis using some unitary
    # from the unitary_noise ensemble. 
    # 
    # Notice that if the basis starts out orthonormal, it ends orthonormal.
    
    # the global dimension:
    dim = len(basis[0])
    assert all((len(b_elem)==dim for b_elem in basis)), "Basis vectors must have the same dimension."
    # unitary sampled from aforementioned ensemble:
    U = unitary_noise(dim,noise_level)
    
    return [U.dot(b_elem) for b_elem in basis]
    
# check that things work:
#    
# sample = unitary_noise(2,10**(-5))
# 
# print("unitary = \n",sample)
# 
# print("\nproof of unitarity: UU^dag =\n",sample.dot(sample.conjugate().transpose()))