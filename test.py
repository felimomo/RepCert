from Certificates.Classes import RepClass as rep
from Certificates.Tools import lin
from Certificates import InvarianceCertificate as inv
from Certificates import IrreducibilityCertificate as irr
from Certificates import BundleCertificate as cert
from ForTesting import randRep as rr
from ForTesting import helperFns as h
from ForTesting.Groups import s3
from ForTesting.Groups import s4

import numpy as np
import string
import math
import cmath
import random
import time

print(#
"""
-o-o-o-o-o-o-o-o-o-o-
  Single Shot Test 
-o-o-o-o-o-o-o-o-o-o-

A single random representation is constructed. The representation is block diagonal in the
standard basis, but the multiplicities are chosen randomly. An irreducible subrep is chosen 
at random and its projector is corrupted by a given small random matrix. This approximate
projector is run through the invariance and irreducibility certificates.

The automatic test sets the group, threshold false-positive prob, and noise level at some
predefined values (see source: test.py).

"""
)
machine_eps = 2**(-52)
t_surplus = 100
automatic = input("Want to automatize? (y/n)")

if automatic=='n':
    test_type = input("Which test would you like? (Opts: s3, s4, s5).\n")
    error_p = eval(input("Threshold false positive probability = "))
    noiseExponent = int(input("Noise level will be 10^(-x), x int, x = "))
    noiseLevel = 10**(-noiseExponent)
elif automatic=='y':
    test_type = 's5'
    error_p = 0.0000001
    noiseLevel = 10**(-12)

scale = eval(input("Scale at which multiplicities are sampled = "))
                                
if test_type == 'pauli':
    n = int(input("n = ")) 
    noiseExp = int(input("Noise level is 10^(-x), x int, x = "))
    noiseLevel = 10**(-noiseExp)
    dens = (0,2*n)
    qb = 0
    pX = np.array([[0,1],[1,0]])
    pZ = np.array([[1,0],[0,-1]])
    id  = np.eye(2)
    
    def trivRep(g,dim):
        return np.eye(dim)
    
    def defRep(g,i,n):
        if i > 0:
            return np.kron( np.kron(np.eye(int(2**(i-1))), g), np.eye(int(2**(n-i))) )
        else:
            return np.kron(g,np.eye(int(2**(n-1))))
        
    def thisRepX(g,i,n):
        #for X type generators
        return h.oplus(h.direct_multiple(defRep(g,i,n), 2), trivRep(g,int(2**n) + 1))
    
    def thisRepZ(g,i,n):
        #for Z type generators
        return h.oplus(h.direct_multiple(defRep(g,i,n), 3), trivRep(g,1))
    
    Xgens = []
    Zgens = []
    Xims = []
    Zims = []
    for i in range(n):
        Xbstr = 'X_0'*(i-1)+'1'+'0'*(n-i)
        Zbstr = 'Z_0'*(i-1)+'1'+'0'*(n-i)
        Xgens.append( rep.group_element(name=Xbstr) )
        Zgens.append( rep.group_element(name=Zbstr) )
        Xims.append(thisRepX(pX,i,n))
        Zims.append(thisRepZ(pZ,i,n))
    
    R = rep.rep_by_generators(3*(2**n)+1, Xgens+Zgens, Xims+Zims, density=dens, q=qb)
    
    invSpacesList = [np.diag( [1]*(2**n)+[0]*(1+2*(2**n)) )]
    for i in range(1+2*(2**n)):
        invSpacesList.append(np.diag([0]*(2**n + i) + [1] + [0]*(2*(2**n) - i) ))
    
    invSpaces = np.array(invSpacesList)
    dim = len(invSpaces[0])
    noiseList = [noiseLevel*np.random.rand(dim,dim) for i in range(len(invSpaces))]
    noisyInvSpaces = invSpaces + np.array(noiseList)
    
    start_time = time.time()
    
    if cert.subrep_tester(R,random.choice(noisyInvSpaces),t_surplus,error_p,prnt=True):
        print("Irreducible!\n")
        print("Computation time = ", time.time() - start_time)
    
if test_type == 's3' :
    t = rep.group_element(name='12')
    c = rep.group_element(name='123')
    generators = [t,c]
    

    
    dim, generators, images, well_cond, noisySpace = rr.rr_repAndInv('s3',generators,noiseLevel,scale=scale)
    
    print("Dimension = ", dim)
    
    R=rep.rep_by_generators(dim,generators,images,density=(well_cond[0],well_cond[1]),q=well_cond[2])
    R.set_groupOrder(6)
    
    start_time = time.time()
    
    if cert.subrep_tester(R,noisySpace,t_surplus,error_p,prnt=True):
        print("Irreducible!\n")
        print("Computation time = ", time.time() - start_time, "s")
    else:
        print("Dont know if irrep!\n")
        print("Computation time = ", time.time() - start_time, "s")

if test_type == 's4':
    t = rep.group_element(name='12')
    c = rep.group_element(name='1234')
    generators = [t,c]
    
    dim, generators, images, well_cond, noisySpace = rr.rr_repAndInv('s4',generators,noiseLevel,scale=scale)
    
    print("Dimension = ", dim)
    
    R=rep.rep_by_generators(dim,generators,images,density=(well_cond[0],well_cond[1]),q=well_cond[2])
    R.set_groupOrder(24)
    
    start_time = time.time()
    
    if cert.subrep_tester(R,noisySpace,t_surplus,error_p,prnt=True):
        print("Irreducible!\n")
        print("Computation time = ", time.time() - start_time, "s")
    else:
        print("Dont know if irrep!\n")
        print("Computation time = ", time.time() - start_time, "s")
    
if test_type == 's5':
    t = rep.group_element(name='12')
    c = rep.group_element(name='12345')
    generators = [t,c]
    
    dim, generators, images, well_cond, noisySpace = rr.rr_repAndInv('s5',generators,noiseLevel,scale=scale)
    
    print("Dimension = ", dim)
    
    R=rep.rep_by_generators(dim,generators,images,density=(well_cond[0],well_cond[1]),q=well_cond[2])
    R.set_groupOrder(120)
    
    start_time = time.time()
    
    if cert.subrep_tester(R,noisySpace,t_surplus,error_p,prnt=True):
        print("Irreducible!\n")
        print("Computation time = ", time.time() - start_time, "s")
    else:
        print("Dont know if irrep!\n")
        print("Computation time = ", time.time() - start_time, "s")
                
if test_type == 'cyclic':
    order = int(input("Order of the cyclic group = "))
    root = cmath.exp(2 * math.pi * 1.j * order**(-1))
    
    wt1 = random.choice([i for i in range(order)])
    wt2 = random.choice([i for i in range(order)])
    wt3 = random.choice([i for i in range(order)])
    
    print(wt1,"\n")
    
    generator = rep.group_element(1,'1')
                
    def irrep(g_element, wt_and_order):
        wt = wt_and_order[0]
        order = wt_and_order[1]
        #returns 1x1 matrix
        return [[cmath.exp(2 * cmath.pi * wt * g_element.element * 1.j * order**(-1))]]             
                
    genRep = h.image_constructor(generator, irrep, 2, irrep, 3, irrep, 3, 
                                 arguments = [[wt1,order], [wt2,order], [wt3,order]]
                                 )
    print("generator = \n", genRep, "\n")
    
    dim = 8            
    delta = 0
    k = order
    q=0
    
    repr = rep.rep_by_generators(dim,[generator],[genRep],density=(delta,k),q=q)            
    
    noiseExponent = int(input("Noise level will be 10^(-x), x int, x = "))
    noiseLevel = 10**(-noiseExponent)
    
    InvSpaces = [   np.diag(2*[1]+6*[0]).astype(complex), 
                    np.diag(2*[0]+3*[1]+3*[0]).astype(complex), 
                    np.diag(5*[0]+3*[1]).astype(complex)
                    ]           
    noisySpace = random.choice( [proj+noiseLevel*np.random.rand(dim,dim) for proj in InvSpaces] )
    
    start_time = time.time()
    
    if cert.subrep_tester(repr,noisySpace,t_surplus,error_p,prnt=True):
        print("Irreducible!\n")  
        print("Computation time = ", time.time() - start_time, "s")
    
    
    
    
    
    
    