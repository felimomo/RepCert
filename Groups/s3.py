import numpy as np
import math

def two_d_rep(g):
    if g.name == '12':
        return np.array([[2**(-1), math.sqrt(2)*3**(-1)],
                        [math.sqrt(2)*3**(-1), -2**(-1)]])
    if g.name == '123':
        return np.array([[-2**(-1), -math.sqrt(2)*3**(-1)],
                        [math.sqrt(2)*3**(-1), -2**(-1)]])
def triv_rep(g):
    return np.array([[1]])

def sign_rep(g):
    if g.name == '12':
        return np.array([[-1]])
    if g.name == '123':
        return np.array([[1]])
        
def parameters():
    return [0,9,0] #[delta, k, q]
