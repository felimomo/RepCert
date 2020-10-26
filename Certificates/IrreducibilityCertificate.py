import numpy as np
import math
import random
from Certificates.Tools import lin, const, rwalk
    
def irr_cert(repr,proj,t,epsilon,error_p):
    #the one and only: yours truly, the certificate
    m = rwalk.number_samples(repr,proj,epsilon,error_p,t)
    et = const.et(repr,epsilon,t,proj)
    dt = const.dt(repr,epsilon,t)
    aux = int(np.trace(proj).real)**2+dt
    aux*= 2*math.log(error_p**(-1))
    
    if et >=2 or m <= aux:
        return False
    
    if m > 10**8:  
        continueAns = input("Number of samples needed is "+str(m)+". Would you like to continue? (Y/N) ")
    
        while continueAns not in ["N","n","No","no","Nope","nope","Y","y","Yes","yes","Yep","yep"]:
            continueAns = input("I didnt understand you. Would you like to continue? (Y/N) ")
        
        if continueAns in ["N","n","No","no","Nope","nope"]:
            return False    
    
    theta = math.sqrt(aux * (m*(2-et))**(-1))
    E = et + rwalk.repRandWalkEstimator(repr,proj,m,t)
    if E < 2*(1-theta):
        return True
    return False
    
    
    
    
        