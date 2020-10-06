import numpy as np
import Tools.RepClass as rep
import Tools.linear as lin
import InvarianceCertificate as inv
import string
import pprint
import helperFns as h

test_type = input("Which test would you like?\n(Opts: Simple Pauli, Large Pauli)\n").lower()

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
                
                
                
if test_type == 'large pauli':
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
    
    
    
    
    
    
                
                
                
                
                
                
                
                
                
                
                
                