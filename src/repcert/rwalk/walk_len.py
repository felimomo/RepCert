import math

def walkLen(repr,setting='promise',t_surplus=0):
    # output = 1/2 random walk length
    #
    # setting: 'promise' (Haar random) vs 'fixed' generator set
    # t_surplus: in the case of setting = 'fixed', output = output + t_surplus
    if setting=='promise':
        return 2+math.ceil(math.log(repr.dimension,2))
        
        
    # else, setting == 'fixed' and I use a cheap trick:
    
    if hasattr(repr, 'density'):
        # in practice the value of t_min below seems too large for practical
        # purposes. Use k/2 + surplus
        
        return math.ceil(0.5*repr.density[1])+t_surplus
        
    # The true bound for 'fixed' setting, which gets horrible quickly
    else:
        t = 0.5 * math.log(repr.dimension-1) 
        t*= ( -math.log(1-repr.density[1]**(-2) * repr.nGens**(-1)) )**(-1) #minimum t from converse result
        t = int(t)
        return t