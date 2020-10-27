import random
import numpy as np
import ForTesting.helperFns as h
from ForTesting.Groups import s3, s4, s5
# from Groups import s3, s4, s5
# import helperFns as h

def rr_multiplicities(group_name,scale=20):
    assert group_name in ['s3','s4','s5'], 'RandRep Multipl. error: Group '+str(group_name)+' not supported.'
    
    if group_name == 's3':
        return [random.randint(1,scale),random.randint(1,scale),random.randint(1,scale)]
    if group_name == 's4':
        return [random.randint(1,scale),random.randint(1,scale),random.randint(1,scale),random.randint(1,scale),random.randint(1,scale)]
    if group_name == 's5':
        return [random.randint(1,scale) for i in range(5)]

def rr_images(group_name,gens,multi):
    assert group_name in ['s3','s4','s5'], 'RandRep Images error: Group '+str(group_name)+' not supported.'
    
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
    
    if group_name == 's5':
        im_t = h.image_constructor(gens[0], s5.triv_rep, multi[0],
                                      s5.sign_rep, multi[1],
                                      s5.d4_rep, multi[2],
                                      s5.d5_rep, multi[3],
                                      s5.d6_rep, multi[4])
        im_c = h.image_constructor(gens[1], s5.triv_rep, multi[0],
                                      s5.sign_rep, multi[1],
                                      s5.d4_rep, multi[2],
                                      s5.d5_rep, multi[3],
                                      s5.d6_rep, multi[4])
    
    return [im_t, im_c]
    
def rr_invSpaces(group_name,multi):
    assert group_name in ['s3','s4', 's5'], 'Inv Space error: Group '+str(group_name)+' not supported.'
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
        
    if group_name == 's5':
        ones = [[1], [1], 4*[1], 5*[1], 6*[1]]
        zeros= [[0], [0], 4*[0], 5*[0], 6*[0]]
        
        def leftzeros(j,multi):
            # print([zeros[i]*multi[i] for i in range(j)])
            return sum([zeros[i]*multi[i] for i in range(j)], [])
        def rightzeros(j,multi):
            # print([zeros[i]*multi[i] for i in range(j+1,len(zeros))])
            return sum([zeros[i]*multi[i] for i in range(j+1,len(zeros))], [])
        def blck(j,multi):
            return [i*zeros[j] + ones[j] + (multi[j]-1-i)*zeros[j] for i in range(multi[j])]
            
        leftzeros(3,multi)
        invS = [[leftzeros(j,multi) + blckrow + rightzeros(j,multi)] for j in range(len(multi)) for blckrow in blck(j,multi)]
        
        return invS
        
        # prelim =    [#
        #             [j, [i*zeros[j] + ones[j] + (multi[j]-i)*zeros[j]]] #
        #             for j in range(6) for i in range(multi[j]) ]
        # invS = prelim[:][1:]
        # for l in range(len(invS)):
        #     for row in prelim:
        #         if row[0] > prelim[l][0]:
        

def rr_repAndInv(group_name,generators,noiseLevel,scale=20): 
    #group stuff:
    if group_name=='s3':
        well_cond = s3.parameters() #[delta, k ,q]
    if group_name=='s4':
        well_cond = s4.parameters() 
    if group_name=='s5':
        well_cond = s5.parameters()
       
    #representation stuff:
    multi = rr_multiplicities(group_name,scale)
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













