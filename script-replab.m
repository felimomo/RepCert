cd ../replab-0.9.0;

replab_init;

% create a group:
% s7 = replab.S(7);
% or
U  = replab.U(2);
s3 = replab.S(3);
% s2 = replab.S(2);
% W  = s2.wreathProduct(s6)
W = s3.wreathProduct(U)
%
% Set generators:
% gen1 = [2 1 3 4 5 6 7];
% gen2 = [2 3 4 5 6 7 1];
% gens = W.generators;

% create rep:
% rep = W.primitiveRep(s6.naturalRep);
rep = W.primitiveRep(kron(U.definingRep,kron(U.definingRep,U.definingRep.conj)))
% complexify (if it is real, for example):
% rep = rep.complexification %-> already complex for unitary group
% Generators in that rep:
% cyclic_perm   = rep.image([2 3 4 5 6 7 1]);
% transposition = rep.image([2 1 3 4 5 6 7]);

% Simultaneously sample generators and set their images:
%
% U4 has a generating set with 3 elements (Hi, Pi, pi/8).
% => prob(5 rand elements of U4 generate U4) = 1. 
% 
% => 9 random elements generate U2 x U2 x U2. 
% 
% Now sample two extra elements to generate S3 Wreath U4. In fact,
% sample three extra elements, just to be sure (2 random elements might
% not quite generate S4 with high prob, because S3 is not too large).    ==> 12 generators (symmetrize set: 24 in total)
i = 1; generators = {}; gen_ims={};
while i < 26
  generators{i} = W.sample;
  generators{i+1} = W.inverse(generators{i});
  gen_ims{i} = rep.image(generators{i});
  gen_ims{i+1} = rep.image(generators{i+1});
  i = i+2;
endwhile

% Generator images
% i = 1; %indexing of generators starts with 1
% gen_ims = {};
% while i < W.nGenerators+1
%   gen_ims{i} = rep.image(W.generators{i});
%   i = i+1;
% endwhile
% decompose rep:
dec = rep.decomposition.nice
% sample random subrep: (first random isotypic component, then random irrep)
randcomp  = dec.component(randi(dec.nComponents));
randirrep = randcomp.irrep(randi(randcomp.nIrreps));
% basis for irrep:
basis = randirrep.basis;

% save files: (v7 is used so scipy can read them being octave outputs)
save -v7 basis.mat basis
save -v7 gen_ims.mat gen_ims
% save -v7 cyclic_perm.mat cyclic_perm
% save -v7 transposition.mat transposition
