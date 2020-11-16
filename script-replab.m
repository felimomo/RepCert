cd ../replab-0.9.0;

replab_init;

% create a group:
% U  = replab.S(3);
% Sn = replab.S(6);
Parties = replab.S(3);
Settings= replab.S(3);
Outcomes= replab.S(2);
X = Settings.wreathProduct(Outcomes);
W = Parties.wreathProduct(X);
% W = Sn.wreathProduct(U)
% W = Sn
%
% Set generators:
% gen1 = [2 1 3 4 5 6 7];
% gen2 = [2 3 4 5 6 7 1];
% gens = W.generators;

% Cayley diam calculation for (Sa wr Sb wr Sc, X := Sb wr Sc):
% 
% diam(X) = diam(Sb) + b*diam(Sc) = 2 + 3*1 = 5
% diam(W) = diam(Sa) + a*diam(X) = 2 + 3*5 = 17

% create rep:
Xrep= X.imprimitiveRep(Outcomes.naturalRep);
rep = W.primitiveRep(Xrep);
% complexify (if it is real):
rep = rep.complexification
% Generators in that rep:
% cyclic_perm   = rep.image([2 3 4 5 6 7 1]);
% transposition = rep.image([2 1 3 4 5 6 7]);

% Simultaneously sample generators and set their images:
%
% if U has u generators and Sn has 2 generators, then the total number of generators
% is n*u + 2. (For Sn \wr U.)

i = 1; 
% generators = {}; 
gen_ims={};
while i < W.nGenerators+1
  % generators{i} = W.sample;
  % generators{i+1} = W.inverse(generators{i});
  gen_ims{i} = rep.image(W.generators{i});
  i = i+1;
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
