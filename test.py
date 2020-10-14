import numpy as np
import Tools.RepClass as rep
import Tools.linear as lin
import InvarianceCertificate as inv
import IrreducibilityCertificate as irr
import string
import math
import pprint
import helperFns as h
import main
import random

test_type = input("Which test would you like? (Opts: pauli, s3, s4).\n")

machine_eps = 2**(-52)
                                
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
    main.subrep_tester(R,random.choice(noisyInvSpaces))
    
if test_type == 's3':
    t = rep.group_element(name='12')
    c = rep.group_element(name='123')
    
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
    
    im_t = h.image_constructor(t,two_d_rep,3,triv_rep,3,sign_rep,3)
    im_c = h.image_constructor(c,two_d_rep,3,triv_rep,3,sign_rep,3)
    
    generators = [t,c]
    images = [im_t,im_c]
    # listify = [list(row) for row in im_t]
    # pprint.pprint(listify)
    
    dim = 12
    delta = 0
    k = 9
    q = 0
    
    R=rep.rep_by_generators(dim,generators,images,density=(delta,k),q=q)
    
    invSpaces = []
    
    noiseExponent = int(input("Noise level will be 10^(-x), x int, x = "))
    noiseLevel = 10**(-noiseExponent)
    pi1 = h.oplus(np.diag([1,1]),np.zeros((10,10)))
    noise = noiseLevel*np.random.rand(dim,dim)
    noisySpace = pi1 + noise
    
    main.subrep_tester(R,noisySpace)

if test_type == 's4':
    t = rep.group_element(name='12')
    c = rep.group_element(name='1234')
    
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
                
    im_t = h.image_constructor(t,aThreeD_rep,1,bThreeD_rep,1,twoD_rep,1)
    im_c = h.image_constructor(c,aThreeD_rep,1,bThreeD_rep,1,twoD_rep,1)
    dim = len(im_t)
    
    delta = 0
    k = 16
    q = 0
    
    R = rep.rep_by_generators(dim,[t,c],[im_t,im_c],density=(delta,k),q=q) 
    
    noiseExponent = int(input("Noise level will be 10^(-x), x int, x = "))
    noiseLevel = 10**(-noiseExponent)
    InvSpaces = [   np.diag(3*[1]+5*[0]).astype(complex), 
                    np.diag(3*[0]+3*[1]+2*[0]).astype(complex), 
                    np.diag(6*[0]+2*[1]).astype(complex)
                    ]           
    noisySpace = random.choice( [proj+noiseLevel*np.random.rand(dim,dim) for proj in InvSpaces] )
      
    main.subrep_tester(R,noisySpace)            
                
                
                
                
                
                