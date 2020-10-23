import numpy as np
import random
import string
    
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
    

class rep_by_generators(generators):
    #representation defined by map from generators to images
    def __init__(self, dimension, generatorSet = [], genImages = [], **kwargs):
        self.dimension = dimension #dimension of representation
        self.nGens = len(generatorSet) #number of generators
        self.Images = dict()
        self.generatorList = []
        
        #keyword args are:  
        #                   density = tuple (delta,k) s.t. generator set is (delta,k)-dense in group,
        #                   q = number s.t. the rep is q-bounded
        
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
        

        
        
#
# Old unused classes:
#
        
        
# class group_element:
#     #element of a group with its name
#     def __init__(self, element=None, name=None):
#         self.element = element
#         if name == None:
#             #generate random name if not provided
#             self.name = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
#         else:
#             self.name = name
# 
# class group_element_image(group_element):
#     #representation image of a group element
#     def __init__(self,g,im):
#         assert isinstance(g,group_element), "First argument should be a group_element object."
#         self.element = g
#         self.Image = {self.element.name:im}
# 
#     def setImage(self,im):
#         assert isinstance(im,list) and isinstance(im[0],list), "Image not a matrix."
#         assert all([len(im)==len(im[i]) for i in range(len(im))]), "Image not a square matrix."
#         self.Image[self.element.name] = im
#         self.dimension = len(im)
        
    