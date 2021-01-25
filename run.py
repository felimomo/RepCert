import readMat
import display as dis
from Certificates import InvarianceCertificate as inv
from Certificates import IrreducibilityCertificate as irr
from Certificates.Classes import RepClass as rep

# Intro to program
dis.run_intro()

########################################################################################
######################################## Input: ########################################
########################################################################################

setting = dis.ask_setting()

# create dictionary { 'basis':basis, 'gen_names':gen_names, 'gen_images':gen_images}
# by reading input file.
rep_dict = readMat.readMatFile()

# create list of group elements out of the list of generator names
generatorSet = list(map(lambda x: rep.group_element(name=x), rep_dict['gen_names']))

# dimension containing the space: just measure # of components of the first basis vector
global_dim = len(rep_dict['basis'][0])

if setting='fixed':
    # user inputs representation parameters ( (delta,k)-density and q-boundedness: see paper).
    (delta,k), q = readMat.inputWellBehaved()
    repr = rep.rep_by_generators(dimension=global_dim,generatorSet=generatorSet,
                                 genImages=rep_dict['gen_images'], 
                                 density=(delta,k), q=q)
else:
    # in this case setting = 'promise'
    repr = rep.rep_by_generators(dimension=global_dim,generatorSet=generatorSet,
                                 genImages=rep_dict['gen_images'])
                
# some ad-hoc number to make sure things converge             
t_surplus = 10
t = set_t(repr,setting,t_surplus)

# probability of false positive (by default set to 10^-7)
thresh = eval(input("Threshold false positive rate = "))
conf   = eval(input("Confidence parameter (approximate f. negative rate) = "))
assert theshh<conf, "Error: confidence parameter must be larger than false positive threshold."

















