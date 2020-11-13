import readMat
from Certificates import BundleCertificate as cert
from Certificates.Classes import RepClass as rep
import time


read_time = time.time()
# create dictionary { 'basis':basis, 'gen_names':gen_names, 'gen_images':gen_images}
# by reading input file.
rep_dict = readMat.readMatFile(automatic=True)

# create list of group elements out of the list of generator names
generatorSet = list(map(lambda x: rep.group_element(name=x), rep_dict['gen_names']))

# user inputs representation parameters ( (delta,k)-density and q-boundedness: see paper).
(delta,k), q = readMat.inputWellBehaved(automatic=True)

# dimension containing the space: just measure # of components of the first basis vector
global_dim = len(rep_dict['basis'][0])
# print(rep_dict['gen_images'][0])
# print(" ")
# print(len(rep_dict['gen_images'][0]))
#
eread_time = time.time()
print("Time reading .mat files: ", eread_time - read_time)

rep_time = time.time()
#
repr = rep.rep_by_generators(dimension=global_dim,generatorSet=generatorSet,genImages=rep_dict['gen_images'], 
                             density=(delta,k), q=q)
# When we look at a finite group:
# repr.set_groupOrder('finite')
# When we look at a Lie group:
repr.make_Lie()

erep_time = time.time()
print("Time constructing rep : ", erep_time - rep_time)
                
# some ad-hoc number to make sure things converge             
t_surplus = 100

# probability of false positive (by default set to 10^-7)
p_error = 0.0000001

cert_time = time.time()

certif = cert.subrep_tester(repr, rep_dict['basis'], t_surplus, p_error, prnt=True)

if certif:
    ecert_time = time.time()
    print("Irreducible!\n")
    print("Time certifying: ", ecert_time-cert_time)