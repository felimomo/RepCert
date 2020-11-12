# Written to be at Replab/RepCert/
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
#
# Now run replab:
octave replab_script.m
echo "Replab script done."
#
# Now move the .mat files:
mv ../replab-0.9.0/*.mat InFiles/
echo "Moving files done."
#
# Finally, run the auto repcert run:
python3 auto_run.py