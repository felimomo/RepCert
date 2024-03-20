import math

def numberSamples(repr,dim,epsilon,error_p,t,conf=None):
    # dim = dimension of subrepresentation being tested
    # error_p = threshold false positive rate
    # conf = confidence parameter (approximate false negative rate)
    # epsilon = invariance certificate precision
    # 2t = length of random walks
    #
    # output = number of random walks sampled
    
    if conf is None:
        # if no confidence parameter is provided, set it to 2*error_p
        conf = 2*error_p
    
    dimfactor = 2*dim**2
    log1 = math.log( error_p**(-1) )
    log2 = math.log( (conf-error_p)**(-1) )
    otherfactor = max(math.ceil(log1),8*math.ceil(log2))
    
    return dimfactor*otherfactor