def run_intro():
    print("""
RepCert: a package which certifies decompositions of compact group representations.
See arXiv:------, www.github.com/RepCert 
Coded by Felipe Montealegre-Mora, Jan 2020.
    
Input files: - InFiles/basis.mat   (matrix of column vectors, basis of subspace to 
                                    be tested)
             - InFiles/gen_ims.mat (list of matrix representations generator images 
                                    of global representation)

Further inputs: 
    - threshold false positive rate, 
    - confidence parameter (approximation to false negative rate), 
      must be > than false positive rate,
    - precision of invariance test, 
    - setting.

setting = 'promise' if generator set is a symmetrized Haar set
setting = 'fixed' else, in which case further parameters are needed to measure how 
          well-behaved the generating set is.
"""
    )

def ask_setting():
    return eval(input("Setting = "))