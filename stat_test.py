import numpy as np
import Tools.RepClass as rep
import Tools.linear as lin
from Groups import s3 
import randRep
# from InvarianceCertificate import *
# from IrreducibilityCertificate import *
import string
import math
import cmath
import helperFns as h
import main
import random

# f = open("OutFiles/output.txt","w+")

#
# statistical tests for s3
#

f = open("OutFiles/s3_stats.txt","w+")
f.write("# Generators: (12), (123)\n---------------------------\n")
f.write("# Noise Exp(x for noise 10^-x), Frac of correctly recognized irreps\n\n")
f.close()

t = rep.group_element(name='12')
c = rep.group_element(name='123')
generators = [t,c]

datapts = 50
min_noiseExp=30
for noiseDoubleExponent in range(10,min_noiseExp-6):
    noiseLevel = 10**(-0.5*(min_noiseExp - noiseDoubleExponent))
    detectedFrac = 0.
    f=open("OutFiles/s3_stats.txt","a")
    
    for i in range(datapts):
        print("    ",end='\r')
        print(i,end='\r')
        multi = randRep.rr_multiplicities('s3')
        images = randRep.rr_images('s3',t,c,multi) #[im_t, im_c]
        dim = len(images[0])
        well_cond = s3.parameters() #[delta, k ,q]
    
        # print("multiplicities = ", multi)
    
        invSpaces = randRep.rr_invSpaces('s3',multi)
        rand_invSpaceList = random.choice(invSpaces)
        rand_invSpace = np.diag(rand_invSpaceList)
        noise = noiseLevel*np.random.rand(dim,dim)
        noisySpace = rand_invSpace+noise
        
        # print("inv subspace = ",invSpaces.index(rand_invSpaceList)) 
        # print(rand_invSpaceList)
    
        R=rep.rep_by_generators(dim,generators,images,density=(well_cond[0],well_cond[1]),q=well_cond[2])
    
        if main.subrep_tester(R,noisySpace):
            # print("in here!")
            detectedFrac += datapts**(-1)
    
    # noise level, detected frac
    f.write(str(0.5*(min_noiseExp - noiseDoubleExponent))+", "+str(detectedFrac)+"\n")
    f.close()
