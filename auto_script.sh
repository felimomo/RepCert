# Written to be at Replab/RepCert/
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
octave ForTesting/replab_script.m
#
# Now move the .mat files:
mv ../replab-0.9.0/*.mat InFiles/
#
# Finally, run the auto repcert run:
python auto_run.py