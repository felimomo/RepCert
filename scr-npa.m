cd ../replab-0.9.0;
replab_init;
cd ../RepCert

n = 2; m = 2; l = 3; 
% n numb parties, m numb measurements, l level heirarchy
% Measurements are fixed to be binary in generatorsNPA.m

% Group, Rep, Decomposition
generators = generatorsNPA(n,m,l);
G = replab.SignedPermutationGroup(length(generators{1}), generators);
rep = G.naturalRep.complexification
dec = rep.decomposition.nice
%
% Cayley:
Gni = G.niceGroup;
cay = replab.bsgs.maximumWordLength(Gni)
% cay   = FactO.maximumWordLength

% get generator images:
i = 1; 
% generators = {}; 
gen_ims={};
while i < G.nGenerators+1
  % generators{i} = W.sample;
  % generators{i+1} = W.inverse(generators{i});
  gen_ims{i} = rep.image(G.generators{i});
  i = i+1;
endwhile

randcomp  = dec.component(randi(dec.nComponents));
randirrep = randcomp.irrep(randi(randcomp.nIrreps));
% basis for irrep:
basis = randirrep.basis;

% Save files:
save -v7 InFiles/basis.mat basis
save -v7 InFiles/gen_ims.mat gen_ims
save -v7 InFiles/cay.mat cay % use the group order for a bound on Cayley diam.