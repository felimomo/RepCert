# Written to be at Replab/RepCert/Scrpt (and run from there)
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
rm ../InFiles/*.mat
#
# Now run replab:
octave script-replab.m
echo "Replab script done."
#
# Now move the .mat files:
mv ../../replab-0.9.0/*.mat ../InFiles/
echo "Moving files done."
#
# Write CayleyDiameter.txt file (right now it's S5 \wreath S3).
touch ../InFiles/CayleyDiameter.txt
echo "11*(2**5)" >> ../InFiles/CayleyDiameter.txt
#
# Finally, run the auto repcert run:
python3 ../autorun.py