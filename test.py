import numpy as np
import Tools.RepClass as rep
import Tools.linear as lin
import InvarianceCertificate as inv
import string
import math
import pprint
import helperFns as h

test_type = input("Which test would you like? (Opts: small pauli, larger pauli, s3).\n")

machine_eps = 2**(-52)

if test_type == "simple pauli":
    x = rep.group_element(name="Pauli X")
    z = rep.group_element(name="Pauli Z")
    repX = np.array([[0,1,0,0,0],
                    [1,0,0,0,0],
                    [0,0,1,0,0],
                    [0,0,0,1,0],
                    [0,0,0,0,1]])
    repZ = np.array([[1,0,0,0,0],
                    [0,-1,0,0,0],
                    [0,0,1,0,0],
                    [0,0,0,-1,0],
                    [0,0,0,0,1]])
                    
    R = rep.rep_by_generators(5,[x,z],[repX,repZ], density=(0,2), q=0)
    
    invSpaces = np.array([np.diag([1,1,0,0,0]),
                np.diag([0,0,1,0,0]),
                np.diag([0,0,0,1,0]),
                np.diag([0,0,0,0,1])])
    dim = len(invSpaces[0])
    noiseList = [machine_eps*np.random.rand(dim,dim) for i in range(len(invSpaces))]
    noisyInvSpaces = invSpaces + np.array(noiseList)
    
    pprint.pprint(noisyInvSpaces[0].dot(noisyInvSpaces[0])-noisyInvSpaces[0])
    
    for r in range(40):
        epsilon = 10**(-5-0.4*r)
        print("\nepsilon = ",epsilon)
        tests = [inv.inv_cert(R,pi,epsilon) for pi in noisyInvSpaces]
        if all(tests):
            print("Invariant!\n\n-------------------")
        else:
            print("Dont know!\n\n-------------------")
                                
if test_type == 'larger pauli':
    n = int(input("n = ")) 
    dens = (0,2*n)
    qb = 0
    pX = np.array([[0,1],[1,0]])
    pZ = np.array([[1,0],[0,-1]])
    id  = np.eye(2)
    Xgens = []
    Zgens = []
    Xims = []
    Zims = []
    
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
    noiseList = [machine_eps*np.random.rand(dim,dim) for i in range(len(invSpaces))]
    # pprint.pprint(invSpaces)
    # pprint.pprint(noiseList)
    # print(len(noiseList))
    # print(len(invSpaces))
    noisyInvSpaces = invSpaces + np.array(noiseList)
    # pprint.pprint(noisyInvSpaces[0][0])
    
    for r in range(40):
        epsilon = 10**(-5-0.4*r)
        print("\nepsilon = ",epsilon)
        tests = [inv.inv_cert(R,pi,epsilon) for pi in noisyInvSpaces]
        if all(tests):
            print("Invariant!\n\n-------------------")
        else:
            print("Dont know!\n\n-------------------")
    
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
    listify = [list(row) for row in im_t]
    # pprint.pprint(listify)
    
    dim = 12
    delta = 0
    k = 9
    q = 0
    
    R=rep.rep_by_generators(dim,generators,images,density=(delta,k),q=q)
    
    invSpaces = []
    
    pi1 = h.oplus(np.diag([1,1]),np.zeros((10,10)))
    noise = machine_eps*np.random.rand(dim,dim)
    noisySpace = pi1 + noise
    
    for r in range(40):
        epsilon = 10**(-5-0.4*r)
        print("\nepsilon = ",epsilon)
        if inv.inv_cert(R,pi1,epsilon):
            print("Invariant!\n\n-------------------")
        else:
            print("Dont know!\n\n-------------------")
    
                
                
                
                
                
                
                
                
                
                
                
                