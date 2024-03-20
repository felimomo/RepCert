import numpy as np
import math

#
# What follows are the constants as defined on sections TBD of the paper
#

def fk(repr,k,projnorm,fl,x):
    #
    # evaluates function f_k(x) as defined in arXiv:-----
    prefactor   = math.pi*math.sqrt(int(projnorm)/2)
    parenthesis = 2**(-k)*projnorm + k*x + 4*k*repr.dim*fl*(1+repr.dim*fl)
    return prefactor * parenthesis

def c1(repr,epsilon):
    fl = 2**(-52)
    x = 2*(epsilon+repr.dimension*fl)*(1+epsilon+repr.dimension*fl)
    x+= repr.dimension*fl*(1+epsilon+repr.dimension*fl)**2
    return x

def c2(repr,epsilon):
    const1 = c1(repr,epsilon)
    return 2*const1*(1+const1)

def dt(repr,epsilon,t):
    const1 = c1(repr,epsilon)
    return (1+const1)**t - 1

def et(repr,epsilon,t,dim):
    const2 = c2(repr,epsilon)
    aux  = (1+const2)**(2*t) - 1
    return aux * (dim**2 + dt(repr,epsilon,2*t))


