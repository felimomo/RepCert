import yaml

def readElementList(fname, element_name) -> dict:
    if fname[-4:] == ".npy":
        import numpy as np
        data = np.load(fname)
        if isinstance(data, dict):
            return {element_name: np.load(fname)[element_name]}
        return {element_name: np.load(fname)}
        
    if fname[-4:] == ".mat":
        #
        # supports MATLAB v4, v6, v7-7.2
        import scipy.io as sio
        mat_data = sio.loadmat(fname)
        return {name: data if name==element_name for name, data in mat_data}


def readBases(input_yaml):
    with open(input_yaml, "r") as stream:
       Inputs  = yaml.safe_load(stream)
    #
    # load list of bases
    bases = {}
    for subrep_name, basis_file in Inputs['subreps'].items():
        bases = {
            **bases, 
            **readElementList(basis_file, subrep_name),
        }

    #
    # orthogonalize them using QR decomp
    bases_QRs = {name: np.linalg.qr(basis.T) for name, basis in bases.items()}
    ortho_bases = {name: QR[0].T for name, QR in bases_QRs.items()}
    
    return ortho_bases

def readGenerators(input_yaml):
    with open(input_yaml, "r") as stream:
       Inputs  = yaml.safe_load(stream)
        
    generators = {}
    for gen_name, gen_file in Inputs['generators'].items():
        bases = {
            **generators, 
            **readElementList(gen_file, gen_name),
        }
    return generators


def readInputs(input_yaml: str):
    with open(input_yaml, "r") as stream:
       Inputs  = yaml.safe_load(stream)

    #
    # load list of bases
    ortho_bases = readBases(input_yaml)

    #
    # load list of generators
    generators = readGenerators(input_yaml)

    convergence_params = Inputs.get('convergence_params', {}) # k:= cayley diameter, delta, q

    return {'bases': ortho_bases, 'generators': generators, 'convergence_params': convergence_params}
    

    
        