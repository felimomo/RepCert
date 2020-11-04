import numpy as np

#
# What follows are the constants as defined on section V.B of the paper
#

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

# previous version with the projector as input
#
# def et(repr,epsilon,t,proj):
#     const2 = c2(repr,epsilon)
#     aux  = (1+const2)**(2*t) - 1
#     dim = int(np.trace(proj).real)
#     return aux * (dim**2 + dt(repr,epsilon,2*t))