# TBD:  change so that it only reads and outputs np arrays.
#       this output can then be interpreted by the main 'run'
#       file into RepClass objects.

# 
# Reads input files of a fixed form:
#   *   Lines starting with '#' are ignored (but as a convention NO COMMENTS ON FIRST LINE)
#   *   The structure of the file is: first parameters of the rep (q, density), then 
#       Generator images, then basis (for the space to be tested).
#   *   the parameters of the rep are in the first line of the document, which will read as:
#       
#       (delta,k),,q
#
#   *   Generator images are input as first a line with their name, and then a blocks of 
#       numbers, each entry separated by a space, such as
#       
#       'gen1'
#       1 0 0 0 0
#       0 0 -1 0 0
#       0 1 0 0 0
#       0 0 0 1.4142 1.4142
#       0 0 0 -1.4142 1.4142
#
#       (Here sqrt(2) is approximated by 1.4142)
#      
#   *   Each generator image is separated by a double coma from the others, the end of the
#       generator section is indicated with a double dot '..', eg:
#
#       'gen1'
#       1 0 0 0 0
#       0 0 -1 0 0
#       0 1 0 0 0
#       0 0 0 1.4142 1.4142
#       0 0 0 -1.4142 1.4142
#       ,,
#       'gen2'
#       1 0 0 0 0
#       0 1 0 0 0
#       0 0 1 0 0
#       0 0 0 1.4142 1.4142
#       0 0 0 -1.4142 1.4142
#       ..
#
#   *   The basis is written right after the '..' line. The basis is presented as a block
#       of numbers as with the generators, and each basis element is a column.
#
#
# in summary, overall structure of the file is:
#
# dim,,(delta,k),,q
# gen name 1
# {{image matrix block of numbers 1}}
# ,,
# gen name 2
# {{image matrix block of numbers 2}}
# ,, 
# gen name n
# {{image matrix block of numbers n}}
# ..
# {{basis block of numbers}}

from os import path
import numpy as np
from Certificates.Classes import RepClass as rep

def erase_coments(l):
    # input: list of strings
    #
    # output: list with all strings starting with '#' eliminated
    return [s for s in l if s[0]!='#']

def generate_rep_image(describing_list):
    # Input:
    #
    # first element of describing_list is the name of the group element,
    # after that, it is a block of numbers describing the representation
    # image. There are no trailing '\n' in the elements of describing_list.
    #
    # Output:
    #
    # list with two elements [g, rep_im], where g is a group_element object,
    # and rep_im is the corresponding matrix representation (np.array)
    g = rep.group_element(name=describing_list[0])
    im = [] # will be image of g
    for i in range(1,len(describing_list)):
        im.append([eval(ch) for ch in describing_list[i].split()]) # split the numbers separated by spaces
    return g, np.array(im)    
    

def get_gens(gen_string):
    # outputs list of group elements (objects of the class group_element) followed
    # by a list of their images (np.array's)
    
    # generate a list of lists  with the generator info. The full list will be 
    #       [gen1, gen2, ...],
    # where each geni is a list of the lines defining a the generator. The first line
    # is the name of the generator, and the rest are its matrix rep.
    gen_str_list = [ gen_info.split('\n') for gen_info in gen_string.split(',,')]
    # eliminate elements corresponding to comment lines:
    gen_str_list = erase_comments(gen_str_list)
    
    generators = []
    images = []
    
    for gen_descriptor in gen_str_list:
        g, im = generate_rep_image(gen_descriptor)
        generators.append(g)
        images.append(im)
    return generators, images
    
            
def separate_gens_basis(fname,fdir):
    # outputs a list of two strings, one containing all the info regarding the generators,
    # another containing the basis.
    # 
    # first line is read and nothing happens (since it only contains parameter info)
    with open(fdir+fname) as f:
        f.readline()    #read first line and do nothing with it
        
        # everything before the '..' line is generators, everything after is basis
        return f.read().split('..\n')


def get_basis(basis_str):
    # output:   list of np.array's, each of which is a basis element
    # 
    # input:    string containing a block of numbers (new lines are represented
    #           by \n of course), each column is a basis vector.
    # 
    
    # separate into lines:
    rows_str = basis_str.split('\n')
    # eliminate comment lines:
    rows_str = erase_comments(rows_str)
    # create block of numbers as list of lists:
    rows = [[eval(ch) for ch in row.split()] for row in rows_str] 
    
    # now rows is a square array which is the transpose of what we want.
    # use zip for transposing:
    #
    # (see https://stackoverflow.com/questions/6473679/transpose-list-of-lists)
    # list applied to zip creates a list of lists (zip creates an iterable),
    # the outer list function is to convert the map object back to a list.
    basis_list = list(map(list,zip(*rows)))
    return [np.array(basis_elem) for basis_elem in basis_list] # each basis element is converted to np array.
    
def get_rep_params(fname,fdir):
    # parameters are the dimension, the density (delta,k), and the q-boundedness q.
    with open(fdir+fname) as f:
        # read first line which should read '(delta,k),,q' (the trailing '\n' is 
        # eliminated by the readline() function
        firstline = f.readline()
        assert ',,' in firstline, "First line not in the format dim,,(delta,k),,q."
        return tuple(eval(x) for x in firstline.split(',,'))
        

def read_input(fname,fdir='InFiles/'):
    assert path.exists(fdir), "Path to input file does not exist."
    
    # reading out generators and putting them into a representation:
    dim, density, q = get_rep_params(fname,fdir)
    [gen_string, basis_string] = separate_gens_basis(fname,fdir)
    gens, ims = get_gens(gen_string)
    repr = rep.rep_by_generators(dimension=dim,generatorSet=gens,genImages=ims,density=density,q=q)
    
    # getting the basis for the subspace
    basis = get_basis(basis_string)
    
    return repr, basis
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
