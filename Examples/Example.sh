# Written to be run from Replab/RepCert
# where Replab/replab-0.9.0/ contains
# RepLab source code.
#
# runs first the replab_script to create a random
# rep and irr. subrep. Then runs RepCert to certify
# the subrep.

# make sure you start in /RepCert
current_dir=${PWD##*/}
if [ "$current_dir" = "Examples" ]; then
  cd ..
fi

echo "RepCert example: decompose a representation with replab, certify random irreducible component."
echo " "
echo "Group images are a symmetrized Haar-sampled set, so the input 'Setting' should be = 'promise'."
echo " "
sleep 1.5

#
#
# First, clean all input files that might interfere:
rm InFiles/*.mat

# now run replab script
octave ForExamples/scr-replab.m
echo "Replab script done."
echo " "

#
# run repcert
python3 run.py