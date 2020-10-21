import numpy as np
import math

def triv_rep(g):
    return np.array([[1]])

def sign_rep(g):
    # Actually both generators get mapped to -1 here
    # (huh, a cyclic permutation of even order having
    # negative sign... that's sketchy but oh well
    return np.array([[-1]])

def twoD_rep(g):
    if g.name == '1234':
        #E3 = math.exp(2*math.pi*1.j/3.)
        E3 = -0.5 + math.sqrt(3)*2**(-1)*1.j
        return np.array([[0,E3**2],[E3,0]])
    if g.name == '12':
        return np.array([[0,1],[1,0]])

def aThreeD_rep(g):
    if g.name == '1234':
        return np.array([ [ -1, 0, 0 ], [ 0, 0, 1 ], [ 0, -1, 0 ] ])
    if g.name == '12':
        return np.array([ [ 0, -1, 0 ], [ -1, 0, 0 ], [ 0, 0, 1 ] ])    
    
def bThreeD_rep(g):
    if g.name == '1234':
        return np.array([ [ 1, 0, 0 ], [ 0, 0, -1 ], [ 0, 1, 0 ] ])
    if g.name == '12':
        return np.array([ [ 0, 1, 0 ], [ 1, 0, 0 ], [ 0, 0, -1 ] ])
        
def parameters():
    return [0,7,0] #[delta, k, q]
    # Cayley graph is the truncated octahedron, generators 1,9
    # in https://en.wikiversity.org/wiki/Symmetric_group_S4
    # Counted by hand and an upper bound on the maximal distance 
    # is 7.