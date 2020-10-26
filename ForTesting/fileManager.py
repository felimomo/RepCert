import random
import string
from os import path
from os import mkdir

def dirName(group_name,avg_dim):
    # returns the location of the out directory
    nice_avg_dim = int(avg_dim) - int(avg_dim)%10
    return 'OutFiles/'+group_name+'/dim'+str(nice_avg_dim)
    
def genDir(name):
    # if the directory is not there, generate directory
    subname = name.split("/dim")[0]
    if not path.exists(subname):
        mkdir(subname)
        mkdir(name)
    if not path.exists(name):
        mkdir(name)

def fileName():
    # generates random file name for an output file 
    fname = ''.join([random.choice(string.ascii_lowercase) for i in range(8)])
    fname+= '.txt'
    return fname


def writeFile(**kwargs):
    group   =   kwargs['group']
    avgd    =   kwargs['avg_dim']    
    maxt    = 2*kwargs['max_t'] #maximal length of random walk
    results =   kwargs['results']
    datapts =   kwargs['data_pts']
    #
    # syntax: [[x1,y1,z1], [x2,y2,z2], ... ] where xi are noise strengths,
    # yi are detected fractions of irreps, and zi are the average number of 
    # samples used for this . (This depends on the maximal t required).
    #
    
    dir = dirName(group,avgd)
    fil = fileName()
    full = dir + '/' + fil
    
    # create dir if not there:
    genDir(dir)
    
    # create file and write:
    f = open(full,'w+')
    f.write(#
    f"""# Group = {group}
# random walks of length at most {maxt}
# avg dimension = {avgd}
# number of random representations averaged over = {datapts}
#
# x, frac, samp : 
#           * noise strength = 10^-x, 
#           * frac = fraction of irreps correctly identified, 
#           * samp = avg total number of samples used.

    """#
    )
    
    for datum in results:
        f.write(str(datum[0])+', '+str(datum[1])+','+str(datum[2])+'\n')
    f.close()

    
    