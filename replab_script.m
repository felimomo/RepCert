cd ../replab-0.9.0;

replab_init;

% create a group:
s6 = replab.S(6);
% or
% s3 = replab.S(3)
% W = s3.wreathProduct(s6)
%
% Set generators
gen1 = [2 1 3 4 5 6];
gen2 = [2 3 4 5 6 1];

% create rep:
nat = s6.naturalRep;
rep = kron(nat,kron(nat,nat));
% complexify (if it is real, for example):
rep = rep.complexification;
% Generators in that rep:
cyclic_perm   = rep.image([2 3 4 5 6 1]);
transposition = rep.image([2 1 3 4 5 6]);

% decompose rep:
dec = rep.decomposition.nice;
% sample random subrep: (first random isotypic component, then random irrep)
randcomp  = dec.component(randi(dec.nComponents));
randirrep = randcomp.irrep(randi(randcomp.nIrreps));
% basis for irrep:
basis = randirrep.basis;

% save files: (v7 is used so scipy can read them being octave outputs)
save -v7 basis.mat basis
save -v7 cyclic_perm.mat cyclic_perm
save -v7 transposition.mat transposition