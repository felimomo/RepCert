cd ../../replab-0.9.0;

replab_init;

% create a group:
% s7 = replab.S(7);
% or
s5 = replab.S(5);
s3 = replab.S(3);
W  = s5.wreathProduct(s3)
%
% Set generators
% gen1 = [2 1 3 4 5 6 7];
% gen2 = [2 3 4 5 6 7 1];
gens = W.generators;

% create rep:
rep = W.primitiveRep(s3.naturalRep);
% complexify (if it is real, for example):
rep = rep.complexification
% Generators in that rep:
% cyclic_perm   = rep.image([2 3 4 5 6 7 1]);
% transposition = rep.image([2 1 3 4 5 6 7]);

% Save generator images
i = 1 %indexing of generators starts with 1
while i < W.nGenerators+1
  save -v7 [mat2str(i) ".mat"] rep.image(W.generators{i});
  i = i+1;
endwhile
% decompose rep:
dec = rep.decomposition.nice;
% sample random subrep: (first random isotypic component, then random irrep)
randcomp  = dec.component(randi(dec.nComponents));
randirrep = randcomp.irrep(randi(randcomp.nIrreps));
% basis for irrep:
basis = randirrep.basis;

% save basis file: (v7 is used so scipy can read them being octave outputs)
save -v7 basis.mat basis
% save -v7 cyclic_perm.mat cyclic_perm
% save -v7 transposition.mat transposition