import numpy as np
import Tools.RepClass as rep
import Tools.linear as lin
from Groups import s3, s4
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

# f = open("OutFiles/s3_stats.txt","w+")
# f.write("# Generators: (12), (123)\n---------------------------\n")
# f.write("# Noise Exp(x for noise 10^-x), Frac of correctly recognized irreps\n\n")
# f.close()
group_name = input('Group to be tested (s3/s4):   ')

if group_name == 's3':
    t = rep.group_element(name='12')
    c = rep.group_element(name='123')
    well_cond = s3.parameters() #[delta, k ,q]

if group_name == 's4':
    t = rep.group_element(name='12')
    c = rep.group_element(name='1234')
    well_cond = s3.parameters() #[delta, k ,q]
    # right now the fact that q in principle depends on rep doesnt give
    # problems since q=0 for all finite groups

generators = [t,c]

datapts = 20
min_noiseExp=18
t_surplus = eval(input("surplus random walk length = ")) #random walks up to length 2(t_min + t_surplus)

f = open("OutFiles/HigherDim/"+group_name+"_t"+str(t_surplus)+"_stats.txt", "w+")
f.write(#
f"""
# Group = {group_name}
# random walks from t_min to t_min+{t_surplus}
# samples = 3 * minimum number of samples
#
# x, frac : noise strength = 10^-x, frac = fraction of irreps correctly identified
"""#
)
f.close()


iteration_counter=0
dimension_adder=0

for noiseDoubleExponent in range(0,min_noiseExp-10):
    noiseLevel = 10**(-0.5*(min_noiseExp - noiseDoubleExponent))
    detectedFrac = 0.
    f=open("OutFiles/HigherDim/"+group_name+"_t"+str(t_surplus)+"_stats.txt","a")
    
    for i in range(datapts):
        print("                                             ",end='\r')
        print(0.5*(min_noiseExp - noiseDoubleExponent)," ",i,end='\r')
        multi = randRep.rr_multiplicities(group_name)
        images = randRep.rr_images(group_name,t,c,multi) #[im_t, im_c]
        dim = len(images[0])
        
        iteration_counter += 1
        dimension_adder += dim
        
        # print("multiplicities = ", multi)
    
        invSpaces = randRep.rr_invSpaces(group_name,multi)
        rand_invSpaceList = random.choice(invSpaces)
        rand_invSpace = np.diag(rand_invSpaceList)
        noise = noiseLevel*np.random.rand(dim,dim)
        noisySpace = rand_invSpace+noise
        
        # print("inv subspace = ",invSpaces.index(rand_invSpaceList)) 
        # print(rand_invSpaceList)
    
        R=rep.rep_by_generators(dim,generators,images,density=(well_cond[0],well_cond[1]),q=well_cond[2])
    
        if main.subrep_tester(R,noisySpace,t_surplus):
            # print("in here!")
            detectedFrac += datapts**(-1)
    
    # noise level, detected frac
    f.write(str(0.5*(min_noiseExp - noiseDoubleExponent))+", "+str(detectedFrac)+"\n")
    f.close()

avg_dimension = float(dimension_adder)/iteration_counter

f=open("OutFiles/HigherDim/"+group_name+"_t"+str(t_surplus)+"_stats.txt","a")
f.write(f"\n\n# Avg dimension = {avg_dimension}")
f.close()
