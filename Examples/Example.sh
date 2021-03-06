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

echo " "
echo "RepCert example: decompose a representation with replab, certify random irreducible component."
echo " "
echo "Group images are a symmetrized Haar-sampled set, so the input 'Setting' should be = 'promise'."
echo " "
sleep 2.5

#
#
# First, clean all input files that might interfere:
rm InFiles/*.mat

echo "Starting RepLAB."
echo " "

# now run replab script
octave Examples/scr-replab.m
echo "RepLAB script done."
echo " "

#
# run repcert
python3 RunRepCert.py