import random
import numpy as np
import ForTesting.helperFns as h
from ForTesting.Groups import s3, s4

def rr_multiplicities(group_name,scale=20):
    assert group_name in ['s3','s4'], 'RandRep Multipl. error: Group '+str(group_name)+' not supported.'
    
    if group_name == 's3':
        return [random.randint(1,scale),random.randint(1,scale),random.randint(1,scale)]
    if group_name == 's4':
        return [random.randint(1,scale),random.randint(1,scale),random.randint(1,scale),random.randint(1,scale),random.randint(1,scale)]

def rr_images(group_name,gens,multi):
    assert group_name in ['s3','s4'], 'RandRep Images error: Group '+str(group_name)+' not supported.'
    
    # gens[0] = t, gens[1] = c
    
    if group_name == 's3':
        im_t = h.image_constructor(gens[0], s3.two_d_rep, multi[0],
                                      s3.triv_rep,  multi[1],
                                      s3.sign_rep,  multi[2])
        im_c = h.image_constructor(gens[1], s3.two_d_rep, multi[0],
                                      s3.triv_rep,  multi[1],
                                      s3.sign_rep,  multi[2])
    if group_name == 's4':
        im_t = h.image_constructor(gens[0], s4.aThreeD_rep, multi[0],
                                      s4.bThreeD_rep, multi[1],
                                      s4.twoD_rep, multi[2],
                                      s4.triv_rep,  multi[3],
                                      s4.sign_rep,  multi[4])
        im_c = h.image_constructor(gens[1], s4.aThreeD_rep, multi[0],
                                      s4.bThreeD_rep, multi[1],
                                      s4.twoD_rep, multi[2],
                                      s4.triv_rep,  multi[3],
                                      s4.sign_rep,  multi[4])
    
    
    return [im_t, im_c]
    
def rr_invSpaces(group_name,multi):
    assert group_name in ['s3','s4'], 'Inv Space error: Group '+str(group_name)+' not supported.'
    if group_name == 's3':
        part1 = [
            i*[0,0] + [1,1] + (multi[0]-i-1)*[0,0] 
              +(multi[1]+multi[2])*[0]
            for i in range(multi[0])
            ]
        part2 = [
             multi[0]*[0,0]
             +i*[0] + [1] +(multi[1]-i-1)*[0]
             +multi[2]*[0]
            for i in range(multi[1])
            ]
        part3 = [
             multi[0]*[0,0] + multi[1]*[0]
             +i*[0] + [1] +(multi[2]-i-1)*[0]
            for i in range(multi[2])
            ]
        return part1 + part2 + part3
        
    if group_name == 's4':
        part1 = [
            i*[0,0,0] + [1,1,1] + (multi[0]-i-1)*[0,0,0] 
              +multi[1]*[0,0,0] + multi[2]*[0,0]
              +(multi[3]+multi[4])*[0]
            for i in range(multi[0])
            ]
        part2 = [
               multi[0]*[0,0,0]
              +i*[0,0,0] + [1,1,1] + (multi[1]-i-1)*[0,0,0] 
              +multi[2]*[0,0]
              +(multi[3]+multi[4])*[0]
            for i in range(multi[1])
            ]
        part3 = [
               multi[0]*[0,0,0] + multi[1]*[0,0,0]
              +i*[0,0] + [1,1] + (multi[2]-i-1)*[0,0] 
              +(multi[3]+multi[4])*[0]
            for i in range(multi[2])
            ]
        part4 = [
               multi[0]*[0,0,0] + multi[1]*[0,0,0] + multi[2]*[0,0]
              +i*[0] + [1] + (multi[3]-i-1)*[0] 
              +multi[4]*[0]
            for i in range(multi[3])
            ]
        part5 = [
             multi[0]*[0,0,0] + multi[1]*[0,0,0] + multi[2]*[0,0] + multi[3]*[0]
            +i*[0] + [1] + (multi[4]-i-1)*[0] 
            for i in range(multi[4])
            ]
            
        return part1 + part2 + part3 + part4 + part5

def rr_repAndInv(group_name,generators,noiseLevel): 
    #group stuff:
    if group_name=='s3':
        well_cond = s3.parameters() #[delta, k ,q]
    if group_name=='s4':
        well_cond = s4.parameters() #[delta, k ,q]
       
    #representation stuff:
    multi = rr_multiplicities(group_name)
    images = rr_images(group_name,generators,multi) #[im_t, im_c]
    dim = len(images[0])
    
    #invariant subspace stuff:
    invSpaces = rr_invSpaces(group_name,multi)
    rand_invSpaceList = random.choice(invSpaces)
    rand_invSpace = np.diag(rand_invSpaceList)
    noise = noiseLevel*np.random.rand(dim,dim)
    noisySpace = rand_invSpace+noise

    # R=rep.rep_by_generators(dim,generators,images,density=(well_cond[0],well_cond[1]),q=well_cond[2])

    return dim, generators, images, well_cond, noisySpace













