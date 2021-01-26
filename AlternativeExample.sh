# Alternative example (without dependency on replab)
#
#

echo " "
echo "Running alternative example for RepCert. The set of group images have been Haar sampled and"
echo "symmetrized, so pick Setting = promise when prompted."
echo " "
echo "Group = S2 wreath S2 wreath S2 (rep = symmetry of I222,222 scenario)"
echo " "
echo " "
sleep 2

#
#
# Copy the alternative-example files to input location
cp ForExamples/Alt_basis.mat InFiles/basis.mat
cp ForExamples/Alt_gen_ims.mat InFiles/gen_ims.mat

#
# run repcert
python3 run.py