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
rm ../replab-0.9.0/*.mat
#
# Now run replab:
octave script-replab.m
echo "Replab script done."
#
# Now move the .mat files:
mv ../replab-0.9.0/basis.mat InFiles/
mv ../replab-0.9.0/gen_ims.mat InFiles/
echo "Moving files done."
#
# Write CayleyDiam.txt file.
rm InFiles/CayleyDiam.txt
touch InFiles/CayleyDiam.txt
#
# k(Sn wreath U) = (Sn diam) + n*{log^2(epsilon^-1) or (U diam)}
#   -> second term is the diameter of U x ... x U [n times]
#   -> first produce element of Sn, then produce one element of each U(2) 
#   -> U^n is normal subgroup, so doing Sn before or after doesn't matter
#   -> log^2 term is Solovay-Kitaev for U=U(2) (assume constant = 1 for the random generator set)
echo "(0, 16), 0" >> InFiles/CayleyDiam.txt 
# less InFiles/CayleyDiam.txt
#
# Finally, run the auto repcert run:
python3 autorun.py