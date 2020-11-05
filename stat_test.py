import numpy as np
from Certificates.Classes import RepClass as rep
from Certificates import BundleCertificate as cert
from Certificates import IrreducibilityCertificate as irr
from Certificates import Tools as tls
from ForTesting.Groups import s3, s4
from ForTesting import randRep as rr
from ForTesting import helperFns as hlp
import ForTesting.fileManager as flm

import string
import math
import cmath
import random
import time

# important input data that is fixed:
error_p = 0.0000001 
datapts = 25
t_surplus = 100

print(#
f"""
-o-o-o-o-o-o-o-o-o-o-
  Statistical Test 
-o-o-o-o-o-o-o-o-o-o-

Test to see the dependence of false negatives on the dimension of the 
representation, the magnitude of the error in the projector onto an irrep (noise 
strength). Furthermore, it keeps track of the average number of samples required 
to test irreducibility.

For each 'noise strength,' {datapts} random representations are sampled (where 
multiplicities are sampled at a given user-set scale). For each of these samples, 
a random irreducible subrep is chosen and corrupted with a random matrix whose 
elements have size 'noise strength'. A noise strength of x means that these
entries have size at most 10^-x.

The fraction of samples for which the certificate correctly outputs 'invariant and 
irreducible' is recorded. 

"""
)

group = input('Group to be tested (s3/s4/s5):   ')
scale = eval(input('Scale at which the multiplicities are sampled: '))

if group == 's3':
    t = rep.group_element(name='12')
    c = rep.group_element(name='123')

if group == 's4':
    t = rep.group_element(name='12')
    c = rep.group_element(name='1234')
    
if group == 's5':
    t = rep.group_element(name='12')
    c = rep.group_element(name='12345')

generators = [t,c]

# constants:
min_noiseExp=30

# initialize dynamic stuff:
data = []
iteration_counter=0
dimension_adder=0
print(" ")
print("-----------------------------------")
print(" noise, frac,    samp,      runtime")
print("-----------------------------------")
print(" ")

for noiseDoubleExponent in range(0,min_noiseExp-8):
    x = 0.5*(min_noiseExp - noiseDoubleExponent)
    noiseLevel = 10**(-x)
    detectedFrac = 0.
    avg_samples = 0.
    avg_time = 0.
    
    for i in range(datapts):
        dim, generators, images, well_cond, noisyBasis = rr.rr_repAndInv(group,generators,noiseLevel,scale=scale)
        
        R=rep.rep_by_generators(dim,generators,images,density=(well_cond[0],well_cond[1]),q=well_cond[2])
        R.set_groupOrder('finite')
        
        iteration_counter += 1
        dimension_adder += dim
        
        start_time = time.time()
        
        #invariance:
        epsilon = cert.best_invariance_certificate(R,noisyBasis)
        
        #irreducibility:
        samples_used = 0
        t_min = cert.minimum_t(R)
        t_max = t_min + t_surplus
        for t in range(t_min,t_max+1):
            samples_used += tls.rwalk.number_samples(R,len(noisyBasis),epsilon,error_p,t)
            
            if irr.irr_cert(R,noisyBasis,t,epsilon,error_p):
                detectedFrac += datapts**(-1)
                break
        end_time = time.time()
        
        avg_time += datapts**(-1) * (end_time-start_time)
        
        avg_samples += datapts**(-1) * samples_used       
    
    data += [[x, detectedFrac, avg_samples, avg_time]]
    print("{:.2f}".format(x), ", " , 
    "{:.2f}".format(detectedFrac), ", " ,
    "{:.2f}".format(avg_samples), ", " ,
    "{:.2f}".format(avg_time), ", " ,
    "(avg dim = ",
    "{:.2f}".format(float(dimension_adder)/iteration_counter),")")

avg_dim = float(dimension_adder)/iteration_counter

flm.writeFile(group=group, avg_dim=avg_dim, max_t=t_max, data_pts=datapts, results=data, error_p=error_p)

# f=open(file,"a")
# f.write(f"\n\n# Avg dimension = {avg_dimension}")
# f.close()
