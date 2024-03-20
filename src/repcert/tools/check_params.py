def checkParams(r,error_p,n):
    # r = number of generators,, error_p = threshold prob of f. positive, n = dimension
    #
    # Safety check for 'promise' setting: in this case, the generator set has to have
    # at least the size of the if clause below. Failing this test indicates that the
    # promise can't be kept.
    #
    
    if r >= 12*math.ceil(math.log(2./error_p) + 2*math.log(n)):
        return True
    else:
        print("Promise setting failure: not enough generators.\n")
        return False
