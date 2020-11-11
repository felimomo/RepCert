import scipy.io as sio
import numpy as np

# Reads .mat files generated by replab using the 'save -v7' command.

def readMatFile(automatic=False):
    # output: dictionary of form {'basis':basis, 'gen_names':gen_names, 'gen_images':gen_images}
    # where gen_images is a list of np.arrays, each of which is a generator image.
    #
    # the order of the list gen_names matches the order of the list gen_images.
    #
    # If automatic==True, I fix the generator file and basis file names to a standard.
    
    if automatic==True:
        basis_file = 'InFiles/basis.mat'
        generator_files = ['InFiles/cyclic_perm.mat', 'InFiles/transposition.mat']
    else:
        basis_file = 'InFiles/'+input('Basis file (.mat format): ')
        generator_file_names = input('Generator files (.mat format, one generator per file, file names separated by a space): ').split()
        generator_files = ['InFiles/'+name for name in generator_file_names]

    assert all((name[-4:]=='.mat' for name in generator_files+[basis_file])), 'Files must be .mat!'

    # Generates np.array such that each subarray is a basis element (the .T is
    # needed because replab outputs the basis using columns for basis elements,
    # and rows are interpreted as the subarrays). 
    #
    # The loadmat function produces a dictionary with some info about the basis,
    # the entry of the dictionary relevant to us is the actual basis elements, 'basis'.
    #
    basis = np.array(sio.loadmat(basis_file)['basis']).T
    
    
    # Generates a list where each element is the result of loadmap(generator_files[i])
    # for different values of i. Each entry is a dictionary.
    #
    generators_long = list(map(sio.loadmat,generator_files))
    
    # Only the last entry of the dictionary is important to us. First we collect the
    # generator names. x is a dictionary, list(x) is a list of the dictionary words,
    # the last element of the list is the generator name we're looking for.
    #
    # generator_names = list(map(lambda x: list(x)[-1]))
    
    # list(x)[-1] is the generator name corresponding to the dictionary x (each dict
    # corresponds to one generator). x[list(x)[-1]] is the corresponding image of 
    # list(x)[-1] --this is according to the format in which Replab save -v7 works.
    #
    # Create list where each list element is of the form [ gen_name, gen_image],
    # where gen_image is an np.array.
    #
    generator_n_i = list(map(lambda x: [list(x)[-1], np.array(x[list(x)[-1]])], generators_long))

    # now create a list of names and list of images separately
    gen_names = [y[0] for y in generator_n_i]
    gen_images = [y[1] for y in generator_n_i]
    
    full = {'basis':basis, 'gen_names':gen_names, 'gen_images':gen_images}

    return full
    
    
def inputWellBehaved(automatic=False):
    # user inputs the well-behaved parameters (denisty (delta,k) and q-boundedness).
    # here (delta,k)-density means that words of length k in the generators approximate
    # up to distance delta (invariant norm in the Lie algebra) any group element. 
    #
    # See accompanying paper for further details (TBD).
    #
    # For finite groups, k=cayley diameter, delta = q = 0.
    #
    # If automatic==True, then set these values to something predetermined here
    # (to make it more ergonomic when the group and generator set is fixed):
    if automatic==True:
        # for S6 with a transposition and cyclic permutation:
        return (0, 18), 0
    
    
    delta = eval(input("delta density parameter: "))
    k = eval(input("k density parameter (Cayley depth for finite case): "))
    q = eval(input("q-boundedness of rep: "))
    
    return (delta, k), q


