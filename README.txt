RepCert: a Python 3 method to certify compact group representations.

Input:
- InFiles/gen_ims.mat where an array of matrix images for a set of group elements is saved
- InFiles/basis.mat where a basis (a matrix of column basis elements) for the tested subspace is saved

Note: for octave, use save -v7 as done in the scr-replab.m script.

Further input:
- setting: 'promise' means gen_ims is a symmetrized Haar set, otherwise use 'fixed'
- entrywise error bound on gen_ims and basis
- precision for invariance test
- false positive rate
- confidence parameter (approx. false negative rate)

--> inputs 2-5 referred to as 'quality parameters'

To certify a subspace, save the .mat files in InFiles and run 'python3 run.py'

EXAMPLES:

Three example decompositions of representations are given in replab-scr.m,
the script main.sh does the following:
- executes replab-scr.m to obtain a decomposition and random irrep block of the example representation
- executes run.py to certify the subspace (in all the examples, setting = 'promise')

Important: For the examples to work, check the first lines of replab-scr.m, 
           you have to direct octave to the location of RepLAB in your computer.
           Currently, the relative location of the RepCert repo and RepLAB is
           the following:
           MotherFolder/RepCert
	   MotherFolder/replab-0.9.0

Have fun, and feel free to write me for feedback/questions!
Felipe Montealegre-Mora
fmonteal@thp.uni-koeln.de
