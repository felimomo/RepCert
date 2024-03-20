import numpy as np
import random
import string

from repcert.lin import restrict
from repcert.io import readGenerators

class groupElement:
    #element of a group with its name
    def __init__(self, element=None, name=None):
        self.element = element
        if name == None:
            #generate random name if not provided
            self.name = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
        else:
            self.name = name


class generators:
    #set of generators of a group
    def __init__(self,generators=None):
        if generators==None:
            self.generatorList  = []
        else:
            assert all([isinstance(gen,group_element) for gen in generators]), 'Generators arent group_elements.'
            self.generatorList = [gen for gen in generators]
    
    def add_generator(self, element=None, name=None):
        self.generatorList.append(group_element(element,name))
        
    def print_generator_names(self):
        for element in self.generatorList:
            print(element.name,"\n")


class repByGenerators(generators):
    # properties:
    #   - dimension
    #   - nGens
    #   - Images (dictionary {generator:image}
    #   - generatorList
    #   - density = (delta, k)
    #   - q = q-boundedness of rep
    #   - order = order of group
    #   - Lie = boolean saying if group is a continuous Lie group (cannot have order in that case)
    #           -> initialized to False by default, needs self.make_Lie to change this
    
    #representation defined by map from generators to images
    def __init__(self, dimension, generatorSet = [], genImages = [], **kwargs):
        self.dimension = dimension #dimension of representation
        self.nGens = len(generatorSet) #number of generators
        self.Images = dict()
        self.generatorList = []
        self.Lie = False 
        
        #keyword args are:  
        #                   'promise' = True/False. Answer to 'is generator set as in the paper (symmetrized Haar set)?
        #                       --> If 'promise', then density and q are not necessary for the algorithm.
        #                   density = tuple (delta,k) s.t. generator set is (delta,k)-dense in group,
        #                   q = number s.t. the rep is q-bounded
        
        # if "setting" in kwargs:
        #     self.setting = kwargs["setting"]
        if "density" in kwargs:
            assert isinstance(kwargs["density"],tuple) and len(kwargs["density"])==2, "Density parameter is not a 2-tuple."
            self.density = kwargs["density"]
        if "q" in kwargs:
            assert isinstance(kwargs["q"],(float,int))
            self.q = kwargs["q"]
        
        for gen in generatorSet:
            self.generatorList.append(gen)
        
        assert len(generatorSet)==len(genImages), "Number of images does not match number of generators."
        assert all([len(genImages[i])==self.dimension for i in range(len(genImages))]), "Images of wrong dimension."
        if len(genImages)>0:
            self.Images = {generatorSet[i].name : genImages[i] for i in range(len(genImages))}
            
        
    def add_generator_image(self,element,repImage):
        assert isinstance(element,group_element)
        self.Images.update({element.name : repImage})
        self.generatorList.append(element)
        self.nGens += 1
    
    def image_list(self):
        return [self.Images[g.name] for g in self.generatorList]
        
    def set_q(self,q):
        self.q = q
    
    def set_density(self,density):
        self.density = density
    
    def set_groupOrder(self,ord):
        self.order = ord
        # for finite groups.
        # could be an actual number, or simply 'finite'
    
    def make_Lie(self):
        assert not hasattr(self,'order'), "Continuous groups cannot have order."
        self.Lie = True

    def restriction_to_subrep(self, basis,setting='promise'):
        # restricts repr to a subrepresentation on the space spanned
        # by basis.
    
        new_ims = [restrict(im,basis) for im in self.image_list()] # new rep images of generators
        dim = len(basis) # new dimension
        
        return repByGenerators(dim, repr.generatorList, new_ims)

    @classmethod
    def load_from_yaml(input_yaml_file):
        #
        # assume haar random generators for now
        generator_dict = readGenerators(input_yaml_file)
        genSet = []
        genIms = []
        for gen_name, gen_im in generator_dict.items():
            genSet.append(gen_name)
            genIms.append(gen_im)
        dimension = np.max(genIms[0].shape)
        return repByGenerators(dimension=dimension, generatorSet=genSet, generatorImages=genIms)
            

        



