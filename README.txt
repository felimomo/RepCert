RepCert: a Python 3 method to certify that a subspace is an irreducible subrepresentation
         of compact group representation.

Input:
- InFiles/gen_ims.mat where an array of matrix images for a set of group elements is saved
- InFiles/basis.mat where a basis (a matrix of column basis elements) for the tested subspace 
  is saved

Note: for octave, use save -v7 as done in the scr-replab.m script.

Further input:
1- setting: 'promise' means gen_ims is a symmetrized Haar set, otherwise use 'fixed'
2- entrywise error bound on gen_ims and basis
3- precision for invariance test
4- bound on false positive rate
5- confidence parameter (false negative rate you'd want -- this is only approximate, and must 
   be > false postitive rate)

--> inputs 2-5 referred to as 'quality parameters' in the code interface.

To certify a subspace, save the .mat files in InFiles and run 'python3 RunRepCert.py'

EXAMPLES:

Example bash scripts are provided in the RepCert/Examples. The script Example.sh runs 
an  example of decomposing a representation using RepLAB and then certifying some random
block. This script has a dependency on RepLAB. Specifically, it does the following 
- executes Examples/replab-scr.m to obtain a decomposition and random irrep block of the 
  example representation
- executes RunRepCert.py to certify the subspace (in all the examples, setting = 'promise')

Notice that in replab-scr.m you can toggle between three different examples.

Important: For Example.sh to work, check the first lines of replab-scr.m ---there 
           you have to direct octave to the location of RepLAB in your computer.
           Currently, the relative location of the RepCert repo and RepLAB is
           the following:
               MotherFolder/
	           RepCert
	           replab-0.9.0
     
For RepLAB, visit https://replab.github.io/replab/

If you don't have RepLAB, you can run AlternativeExample.sh. This example uses the files 
Alt_basis.mat and Alt_gen_ims.mat as input (no need to move these files to the input 
subdirectory, the script does that).



Have fun, and feel free to write me for feedback/questions!
Felipe Montealegre-Mora
fmonteal@thp.uni-koeln.de
