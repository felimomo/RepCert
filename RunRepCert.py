import time
import readMat
import display as dis
from Certificates.Tools import rwalk, lin
from Certificates import InvarianceCertificate as inv
from Certificates import IrreducibilityCertificate as irr
from Certificates.Classes import RepClass as rep

# Intro to program
print("""
RepCert: a package which certifies decompositions of compact group representations.
See arXiv:------, www.github.com/RepCert 
Coded by Felipe Montealegre-Mora, Jan 2020.

Input files: - InFiles/basis.mat   (matrix of column vectors, basis of subspace to 
                                be tested)
         - InFiles/gen_ims.mat (list of matrix representations generator images 
                                of global representation)

Further inputs: 
- threshold false positive rate, 
- confidence parameter (approximation to false negative rate), 
  must be > than false positive rate,
- precision of invariance test, 
- setting.

setting = 'promise' if generator set is a symmetrized Haar set
setting = 'fixed' else, in which case further parameters are needed to measure how 
      well-behaved the generating set is.
"""
)

########################################################################################
################################### User Input: ########################################
########################################################################################

setting = input("Setting = ")
fl=0

if input("Use standard choice for quality parameters? (y/n) ") == "y":
    fl = 2**(-52)
    thresh = 0.0000001
    conf   = 0.0000002
    epsilon = 0.00000001
    print(f"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%% Standard quality parameter values: %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                          
Error bound on basis/group images (entrywise) = {fl}
Threshold false positive rate = {thresh}
Confidence parameter (approx false negative rate) = {conf}
Precision of invariance test = {epsilon}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
    )

else:
    # error bound on matrix coefficients of rep:
    fl = eval(input("Error bound on rep. matrix and basis coefficients = "))

    # probability of false positive (by default set to 10^-7)
    thresh = eval(input("Threshold false positive rate = "))
    # conf   = eval(input("Confidence parameter (approximate f. negative rate) = "))
    conf = 2*thresh # temporarily
    assert thresh < conf, "Error: confidence parameter must be larger than false positive threshold."

    # invariance precision:
    epsilon = eval(input("Invariance precision (max Frob. distance to invariant proj.) = "))


########################################################################################
########################### File Input / Preprocessing: ################################
########################################################################################

# create dictionary { 'basis':basis, 'gen_names':gen_names, 'gen_images':gen_images}
# by reading input file.
rep_dict = readMat.readMatFile(True)

# create list of group elements out of the list of generator names
generatorSet = list(map(lambda x: rep.group_element(name=x), rep_dict['gen_names']))

global_dim = len(rep_dict['basis'][0])  # number of components of vectors
dim = len(rep_dict['basis'])            # number of vectors in basis
basis = rep_dict['basis']

# create projector onto subspace:
proj = lin.toproj(basis)
# print(basis)

# worst-case error on the projector: (modify fl from before)
fl = 2*dim*(fl + fl**2)

# create RepClass object
if setting=='fixed':
    # user inputs representation parameters ( (delta,k)-density and q-boundedness: see paper).
    (delta,k), q = readMat.inputWellBehaved()
    repr = rep.rep_by_generators(dimension=global_dim,generatorSet=generatorSet,
                                 genImages=rep_dict['gen_images'], 
                                 density=(delta,k), q=q)
else:
    # in this case setting = 'promise'
    repr = rep.rep_by_generators(dimension=global_dim,generatorSet=generatorSet,
                                 genImages=rep_dict['gen_images'])
                                 
########################################################################################
#################################### Printing: #########################################
########################################################################################

print(f"""
Global dimension = {global_dim}
Subsp. dimension = {dim}
Numb. generators = {len(generatorSet)}
Repr. Mat./Projector coefficient error bound = {fl}
""")
    
########################################################################################
############################# Invariance Certificate: ##################################
########################################################################################            

inv_init = time.time()
if inv.inv_cert(repr,proj,epsilon,thresh,fl,setting):
    print("Invariant!")
    print("(Inv. Cert. time = ", time.time()-inv_init, " s)\n")
else:
    print("Don't know if invariant :(\n")
    import sys
    sys.exit()

########################################################################################
########################### Irreducibility Certificate: ################################
########################################################################################  

irr_init = time.time()  

def restrict_to_subrep(repr,basis,setting='promise'):
    # restricts repr to a subrepresentation on the space spanned
    # by basis.

    new_ims = [lin.restrict(im,basis) for im in repr.image_list()] # new rep images of generators
    dim = len(basis) # new dimension
    
    if setting=='promise':
        return rep.rep_by_generators(dim, repr.generatorList, new_ims)
    # else:
    #     # setting = 'fixed'
    #     return rep.rep_by_generators(dim, repr.generatorList, new_ims, density = repr.density, q = repr.q)

# subrepresentation on which random walk happens:
restr_init = time.time()
subrep = restrict_to_subrep(repr,basis)
print("Restriction to subrep done (in ", time.time()-restr_init, " s)\n")

irr_init = time.time()
if irr.irr_cert(subrep,epsilon,thresh,conf,setting):
    print("Irreducible!\n")
    print("(Irr. Cert. time = ", time.time()-irr_init, " s)\n")
else:
    print("Don't know of irreducible :'(")













