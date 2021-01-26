# Alternative example (without dependency on replab)
#
#

echo "Running alternative example for RepCert. The set of group images have been Haar sampled and"
echo "symmetrized, so pick setting='promise' when prompted."
echo " "
sleep 2

#
#
# Copy the alternative-example files to input location
cp Alt_basis.mat InFiles/basis.mat
cp Alt_gen_ims.mat InFiles/gen_ims.mat

#
# run repcert
python3 run.py