import numpy as np
import math
import random
import helperFns as h

def repRandWalk(repr,t,proj):
    P = np.asmatrix(proj)
    w = np.eye(repr.dimension).astype(complex)
    for i in range(t):
        w *= P*np.asmatrix(random.choice(repr.image_list()))*P.H
    return w

def repRandWalkEstimator(repr,proj,m,t):
    #estimator for random walk of length 2t
    est = 0
    for i in range(m):
        est += abs(np.trace(repRandWalk(repr,t,proj)))**2 * m**(-1)
    return est
    
def number_samples(repr,proj,epsilon,error_p,t):
    dim = int(np.trace(proj).real)
    minimum = 2*math.log(error_p**(-1))
    dt = h.dt(repr,epsilon,2*t)
    minimum*= dim**2 + dt #Minimum m such that irr_cert doesnt abort
    extra_factor = 3 #To be sure that we have enough samples
    return int(extra_factor*minimum)
    
def irr_cert(repr,proj,t,epsilon,error_p):
    #the one and only: yours truly, the certificate
    m = number_samples(repr,proj,epsilon,error_p,t)
    et = h.et(repr,epsilon,t,proj)
    dt = h.dt(repr,epsilon,t)
    aux = int(np.trace(proj).real)**2+dt
    aux*= 2*math.log(error_p**(-1))
    
    if et >=2 or m <= aux:
        return False
        
    continueAns = input("Number of samples needed is "+str(m)+". Would you like to continue? (Y/N) ")
    
    while continueAns not in ["N","n","No","no","Nope","nope","Y","y","Yes","yes","Yep","yep"]:
        continueAns = input("I didnt understand you. Would you like to continue? (Y/N) ")
        
    if continueAns in ["N","n","No","no","Nope","nope"]:
        return False
        
    
    theta = math.sqrt(aux * (m*(2-et))**(-1))
    E = et + repRandWalkEstimator(repr,proj,m,t)
    if E < 2*(1-theta):
        return True
    return False
    
    
    
    
        