# Alternative example (without dependency on replab)
#
#

#
#
# Copy the alternative-example files to input location
cp Alt_basis.mat InFiles/
cp Alt_gen_ims.mat InFiles/
mv InFiles/Alt_basis.mat basis.mat
mv InFiles/Alt_gen_ims.mat gen_ims.mat

#
# run repcert
python3 run.py