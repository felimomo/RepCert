import numpy as np

# functions that are useful for constructing explicit representation examples

def right_pad(A,k):
    #pad each row of the matrix A with k zeroes to the right
    B = []
    for a in A:
        # print(a)
        # print(list(a))
        # print([0.]*k)
        # print(list(a)+[0.]*k,"\n")
        B.append(list(a)+[0]*k)
    return np.array(B)

def left_pad(A,k):
    #pad rows of A with k zeroes on the left
    B = []
    for a in A:
        B.append([0]*k+list(a))
    return np.array(B)

# def down_pad(A,k):
#     #pad each column of A with k zeroes below
#     return horizontal_pad(A.T,k).T

def oplus(A,B=None):
    # returns block matrix 
    # [ A 0]
    # [ 0 B]
    if B is None:
        return A
    else:    
        kA = len(B[0])
        kB = len(A[0])
        assert kA > 0 and kB > 0, 'Matrices must not be empty (must be at least 1x1).'
        A_block = right_pad(A,kA)
        B_block = left_pad(B,kB)
        return np.array(list(A_block)+list(B_block))

def direct_sum(*argv):
    assert len(argv)>0,'At least one argument needed for the direct sum.'
    outMat = argv[0]
    for arg in argv[1:]:
        outMat = oplus(outMat,arg)
    return outMat
    
def direct_sum_list(l):
    assert len(l)>0,'At least one argument needed for the direct sum.'
    outMat = l[0]
    for mat in l[1:]:
        outMat = oplus(outMat,mat)
    return outMat

def direct_multiple(A,m):
    #direct sum of A with itself m times
    outMat = A
    for i in range(m-1):
        outMat = oplus(outMat,A)
    return outMat
    
def image_constructor(g,*argv,**kwargs):
    # the arguments are a set of functions that produce images
    # of a group element g under certain pre-defined representations.
    # 
    # Syntax: 
    #
    # * argv's are fn1, multiplicity1, fn2, multiplicity2, ..., fnk, multiplicityk
    # * kwargs are 
    #      arguments     = list of lists, the i-th row are the extra parameters
    #                      passed to fni. 
    assert len(argv)%2==0,'image_constructor args are: repFn1, multiplicty 1, repFn2, multiplicity 2, ...'
    
    multi  = []
    repFns = []
    for i in range(len(argv)):
        if i%2==0:
            repFns.append(argv[i])
        if i%2==1:
            multi.append(argv[i])
    

    if len(kwargs)==0:
        imageList = [direct_multiple( repFns[i](g) ,  multi[i]) for i in range(len(repFns))]
        return direct_sum_list(imageList)

    arguments = kwargs['arguments'] # list of lists
    assert len(arguments) == len(repFns), "There must be one sublist of arguments per function in the image constructor."    
    
    imageList = [direct_multiple( repFns[i](g,arguments[i]) ,  multi[i]) for i in range(len(repFns))]
    return direct_sum_list(imageList)
    







