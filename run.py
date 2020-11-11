import readMat
from Certificates import BundleCertificate as cert
from Certificates.Classes import RepClass as rep

# create dictionary { 'basis':basis, 'gen_names':gen_names, 'gen_images':gen_images}
# by reading input file.
rep_dict = readMat.readMatFile()

# create list of group elements out of the list of generator names
generatorSet = list(map(lambda x: rep.group_element(name=x), rep_dict['gen_names']))

# user inputs representation parameters ( (delta,k)-density and q-boundedness: see paper).
(delta,k), q = readMat.inputWellBehaved()

# dimension containing the space: just measure # of components of the first basis vector
global_dim = len(rep_dict['basis'][0])

repr = rep.rep_by_generators(dimension=global_dim,generatorSet=generatorSet,genImages=rep_dict['gen_images'], 
                             density=(delta,k), q=q)

# differentiate finite groups for short RWalks.             
if input('Is the group finite? (y/n) ')=='y':
    repr.set_groupOrder('finite')
                
# some ad-hoc number to make sure things converge             
t_surplus = 100

# probability of false positive (by default set to 10^-7)
p_error = 0.0000001

if cert.subrep_tester(repr, rep_dict['basis'], t_surplus, p_error, prnt=True):
    print("Irreducible!\n")
