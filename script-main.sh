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
# Write CayleyDiameter.txt file (right now it's S5 \wreath S3).
rm InFiles/CayleyDiam.txt
touch InFiles/CayleyDiam.txt
echo "(10**(-10), 2* 10**(2*2))" >> InFiles/CayleyDiam.txt #uff that's bad, well let's see
# less InFiles/CayleyDiam.txt
#
# Finally, run the auto repcert run:
python3 autorun.py