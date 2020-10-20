import random
import helperFns as h
from Groups import s3

def rr_multiplicities(group_name):
    assert group_name in ['s3'], 'RandRep Multipl. error: Group '+str(group_name)+' not supported.'
    return [random.randint(1,10),random.randint(1,10),random.randint(1,10)]

def rr_images(group_name,t,c,multi):
    assert group_name in ['s3'], 'RandRep Images error: Group '+str(group_name)+' not supported.'
    
    
    im_t = h.image_constructor(t, s3.two_d_rep, multi[0],
                                  s3.triv_rep,  multi[1],
                                  s3.sign_rep,  multi[2])
    im_c = h.image_constructor(c, s3.two_d_rep, multi[0],
                                  s3.triv_rep,  multi[1],
                                  s3.sign_rep,  multi[2])
    
    return [im_t, im_c]
    
def rr_invSpaces(group_name,multi):
    assert group_name in ['s3'], 'Inv Space error: Group '+str(group_name)+' not supported.'
    
    part1 = [
            [ i*[0,0] + [1,1] + (multi[0]-i-1)*[0,0] 
              +(multi[1]+multi[2])*[0]
            ] 
            for i in range(multi[0])]
    part2 = [
            [ multi[0]*[0,0]
             +i*[0] + [1] +(multi[1]-i-1)*[0]
             +multi[2]*[0]
            ] 
            for i in range(multi[1])]
    part3 = [
            [ multi[0]*[0,0] + multi[1]*[0]
             +i*[0] + [1] +(multi[2]-i-1)*[0]
            ] 
            for i in range(multi[2])]
            
    return part1 + part2 + part3
    