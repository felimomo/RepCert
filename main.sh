# Written to be run from Replab/RepCert
# where Replab/replab-0.9.0/ contains
# RepLab source code.
#
# runs first the replab_script to create a random
# rep and irr. subrep. Moves the files to InFiles,
# and finally runs the auto_run to certify 
# invariance/irreducibility.
#
#
# First, clean all input files that might interfere:
rm InFiles/*.mat
# rm ../replab-0.9.0/*.mat
#
# Now run replab:
# octave scr-replab.m
octave scr-replab.m
echo "Replab script done.\n"
echo "Group images are a symmetrized Haar-sampled set."
# mv *.mat InFiles/
#
# Now move the .mat files (check if cay.mat exists):
# FILE=../replab-0.9.0/cay.mat
# if test -f "$FILE" ; then
#   mv ../replab-0.9.0/cay.mat InFiles/cay.mat
# fi
# mv ../replab-0.9.0/basis.mat InFiles/
# mv ../replab-0.9.0/gen_ims.mat InFiles/
# echo "Moving files done."
#
# 
# FILE=InFiles/cay.mat
# if ! test -f "$FILE"; then
#   #
#   # Write CayleyDiam.txt file.
#   rm InFiles/CayleyDiam.txt
#   touch InFiles/CayleyDiam.txt
#   #
#   # k(Sn wreath U) = (Sn diam) + n*{log^2(epsilon^-1) or (U diam)}
#   #   -> second term is the diameter of U x ... x U [n times]
#   #   -> first produce element of Sn, then produce one element of each U(2) 
#   #   -> U^n is normal subgroup, so doing Sn before or after doesn't matter
#   #   -> log^2 term is Solovay-Kitaev for U=U(2) (assume constant = 1 for the random generator set)
#   #
#   # q-boundedness: dim*r, where dim is the dimension, r is the maximum weight length.
#   #     -> max w length UxU =< 2*max w length U (all extremal weights have same
#   #       length --they're Weyl rotations of each other--, one such extremal
#   #       weight is the highest weight = tensor product of the two higest weights).
#   #
#   echo "(10**(-10), 2+3*100), 2*" >> InFiles/CayleyDiam.txt 
# fi
#
# Finally, run the auto repcert run:
python3 run.py