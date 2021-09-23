import time
import ForTests_ReadMat as read
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

def restrict_to_subrep(repr,basis,setting='promise'):
    # restricts repr to a subrepresentation on the space spanned
    # by basis.

    new_ims = [lin.restrict(im,basis) for im in repr.image_list()] # new rep images of generators
    dim = len(basis) # new dimension
    
    return rep.rep_by_generators(dim, repr.generatorList, new_ims)

########################################################################################
################################### User Input: ########################################
########################################################################################

setting = input("Setting = ")
flo=0
GroupName="S3wrS2wrS3"

if input("Use standard choice for quality parameters? (y/n) ") == "y":
    flo = 2**(-52)
    thresh = 0.0000001
    conf   = 0.0000002
    epsilon = 0.00000001
    print(f"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%% Standard quality parameter values: %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                          
Error bound on basis/group images (entrywise) = {flo}
Threshold false positive rate = {thresh}
Confidence parameter (approx false negative rate) = {conf}
Precision of invariance test = {epsilon}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
    )

else:
    # error bound on matrix coefficients of rep:
    flo = eval(input("Error bound on rep. matrix and basis coefficients = "))

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
rep_dict = read.readMatFileTests(GroupName)
bases = rep_dict['bases']

# create list of group elements out of the list of generator names
generatorSet = list(map(lambda x: rep.group_element(name=x), rep_dict['gen_names']))

global_dim = len(bases[0][0])  # number of components of vectors
print("global dim = ", global_dim)

# create RepClass object
repr = rep.rep_by_generators(dimension=global_dim,generatorSet=generatorSet,
                             genImages=rep_dict['gen_images'])

file=open(r"benchmark_"+GroupName,"a")
file.write(r"# Benchmark results for G = "+GroupName+"\n")
file.write(f"""# Parameters:
# Global dimension = {global_dim}
# Numb. generators = {len(generatorSet)}
# Error bound on basis/group images (entrywise) = {flo}
# Precision of invariance test = {epsilon}
# Threshold false positive rate = {thresh}
# Confidence parameter (approx false negative rate) = {conf}\n
""")
file.write(r"# IrrD & Inv. Time & Restr. Time & Cert. Time & Cert?")


for basis in bases:
    dim = len(basis)
    file.write(f"{dim}"+" & ")
    if dim < 200:
        #only look at small enough reps
        # create projector onto subspace:
        proj = lin.toproj(basis)

        # worst-case error on the projector: (modify flo from before)
        fl = 2*dim*(flo + flo**2)
        
                                     
        ##################################################################################
        #################################### Printing: ###################################
        ##################################################################################
        print("\nNEXT SUBSPACE")
        print(f"""
        Global dimension = {global_dim}
        Subsp. dimension = {dim}
        Numb. generators = {len(generatorSet)}
        Repr. Mat./Projector coefficient error bound = {fl}
        """)

        ##################################################################################
        ############################# Invariance Certificate: ############################
        ##################################################################################

        inv_init = time.time()
        InvCert=inv.inv_cert(repr,proj,epsilon,thresh,fl,setting)
        InvTime = time.time()-inv_init
        file.write(f"{InvTime}"[0:4]+" & ")
        if InvCert:
            print("Invariant!")
            print("(Inv. Cert. time = ", InvTime, " s)\n")
        else:
            print("Don't know if invariant :(\n")
            # import sys
            # sys.exit()
        
        ##################################################################################
        ########################### Irreducibility Certificate: ##########################
        ##################################################################################
        if InvCert:  
            # subrepresentation on which random walk happens:
            restr_init = time.time()
            subrep = restrict_to_subrep(repr,basis)
            restr_time = time.time()-restr_init
            print("Restriction to subrep done (in ", restr_time, " s)\n")
            file.write(f"{restr_time}"[0:4]+" & ")

            irr_init = time.time()
            if irr.irr_cert(subrep,epsilon,thresh,conf,setting):
                irr_time = time.time()-irr_init
                file.write(f"{irr_time} "[0:4]+" & Yes\n")
                print("Irreducible!")
                print("(Irr. Cert. time = ", irr_time, " s)\n")
            else:
                file.write(f"{irr_time} "[0:4]+" & No\n")
                print("Don't know of irreducible :'(")


file.close()












